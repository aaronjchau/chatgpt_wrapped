from datetime import datetime, timedelta, timezone

global_stats = {
    "total_convos": 0,
    "total_msgs_sent": 0,
    "total_words_sent": 0,
    "total_msgs_recd": 0,
    "total_words_recd": 0,
}

conversation_stats = {}

model_stats = {}

msgs_sent_by_hour = {}
msgs_sent_by_day = {}
msgs_sent_by_month = {}
msgs_sent_by_year = {}
msgs_sent_by_date = {}

rolling_12_months = {}

time_stats = {}

days_of_week = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
]

months_of_year = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
]

est_timezone = timezone(timedelta(hours=-5))


def reset_stats():
    global_stats["total_convos"] = 0
    global_stats["total_msgs_sent"] = 0
    global_stats["total_words_sent"] = 0
    global_stats["total_msgs_recd"] = 0
    global_stats["total_words_recd"] = 0
    conversation_stats.clear()
    model_stats.clear()
    msgs_sent_by_hour.clear()
    msgs_sent_by_day.clear()
    msgs_sent_by_month.clear()
    msgs_sent_by_year.clear()
    msgs_sent_by_date.clear()
    rolling_12_months.clear()
    time_stats.clear()

    for hour in range(24):
        msgs_sent_by_hour[str(hour)] = 0

    for day in days_of_week:
        msgs_sent_by_day[day] = 0

    for month in months_of_year:
        msgs_sent_by_month[month] = 0


# compute stats for all messages
def compute_stats(all_messages_props):
    reset_stats()

    for message in all_messages_props:
        convo_id = message["conversation_id"]

        # if this is a new convo, set up new dict for it
        if convo_id not in conversation_stats:
            conversation_stats[convo_id] = {
                "convo_msgs_sent": 0,
                "convo_words_sent": 0,
                "convo_msgs_recd": 0,
                "convo_words_recd": 0,
            }

            # include conversation in global count
            global_stats["total_convos"] += 1

        if message["role"] == "user":
            compute_user_stats(message)

        if message["role"] == "assistant":
            compute_ai_stats(message)

    compute_rolling_12_months()
    time_stats["msgs_sent_by_hour"] = msgs_sent_by_hour
    time_stats["msgs_sent_by_day"] = msgs_sent_by_day
    time_stats["msgs_sent_by_month"] = msgs_sent_by_month
    time_stats["msgs_sent_by_year"] = msgs_sent_by_year
    time_stats["rolling_12_months"] = rolling_12_months

    return global_stats, conversation_stats, model_stats, time_stats


# compute stats for messages sent
def compute_user_stats(message):
    # increment sent message count for this conversation
    conversation_stats[message["conversation_id"]]["convo_msgs_sent"] += 1

    # sum words in total sent word count for this conversation
    word_count = len(message["text"].split())
    conversation_stats[message["conversation_id"]]["convo_words_sent"] += word_count

    # include message sent count in global count
    global_stats["total_msgs_sent"] += 1

    # include word count in global count
    global_stats["total_words_sent"] += word_count
    compute_time_stats(message)


def compute_time_stats(message):
    create_time = message["create_time"]

    if create_time is None:
        return

    try:
        message_time_utc = datetime.fromtimestamp(float(create_time), tz=timezone.utc)
    except (ValueError, TypeError, OSError, OverflowError):
        return

    message_time_est = message_time_utc.astimezone(est_timezone)

    hour = str(message_time_est.hour)
    day = days_of_week[message_time_est.weekday()]
    month = months_of_year[message_time_est.month - 1]
    year = str(message_time_est.year)
    date = message_time_est.date().isoformat()

    msgs_sent_by_hour[hour] += 1
    msgs_sent_by_day[day] += 1
    msgs_sent_by_month[month] += 1
    msgs_sent_by_year[year] = msgs_sent_by_year.get(year, 0) + 1
    msgs_sent_by_date[date] = msgs_sent_by_date.get(date, 0) + 1


def compute_rolling_12_months():
    if msgs_sent_by_date:
        end_date = datetime.fromisoformat(max(msgs_sent_by_date)).date()
    else:
        end_date = datetime.now(est_timezone).date()

    start_date = end_date - timedelta(days=364)
    daily_counts = []

    current_date = start_date
    while current_date <= end_date:
        date_key = current_date.isoformat()
        daily_counts.append(
            {
                "date": date_key,
                "count": msgs_sent_by_date.get(date_key, 0),
            }
        )
        current_date += timedelta(days=1)

    rolling_12_months["start_date"] = start_date.isoformat()
    rolling_12_months["end_date"] = end_date.isoformat()
    rolling_12_months["daily_counts"] = daily_counts

# compute stats for messages received
def compute_ai_stats(message):
    # if there's no message, don't include it because chatGPT always responds at least some text
    if not message["text"]:
        return

    # if there's no model id, it probably was a regenerated message so skip it
    model_id = message["model_id"]
    if not model_id:
        return
    # otherwise include it in the total count for each AI model
    else:
        model_stats[model_id] = model_stats.get(model_id, 0) + 1
    
    conversation_stats[message["conversation_id"]]["convo_msgs_recd"] += 1

    word_count = len(message["text"].split())
    conversation_stats[message["conversation_id"]]["convo_words_recd"] += word_count

    global_stats["total_msgs_recd"] += 1

    global_stats["total_words_recd"] += word_count
