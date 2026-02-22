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
msgs_sent_rolling_12mo = []


def reset_stats():
    global global_stats
    global conversation_stats
    global model_stats
    global msgs_sent_by_hour
    global msgs_sent_by_day
    global msgs_sent_by_month
    global msgs_sent_by_year
    global msgs_sent_by_date
    global msgs_sent_rolling_12mo

    global_stats = {
        "total_convos": 0,
        "total_msgs_sent": 0,
        "total_words_sent": 0,
        "total_msgs_recd": 0,
        "total_words_recd": 0,
    }

    conversation_stats = {}
    model_stats = {}

    msgs_sent_by_hour = {format_hour_label(hour): 0 for hour in range(24)}
    msgs_sent_by_day = {
        "Monday": 0,
        "Tuesday": 0,
        "Wednesday": 0,
        "Thursday": 0,
        "Friday": 0,
        "Saturday": 0,
        "Sunday": 0,
    }
    msgs_sent_by_month = {
        "January": 0,
        "February": 0,
        "March": 0,
        "April": 0,
        "May": 0,
        "June": 0,
        "July": 0,
        "August": 0,
        "September": 0,
        "October": 0,
        "November": 0,
        "December": 0,
    }
    msgs_sent_by_year = {}
    msgs_sent_by_date = {}
    msgs_sent_rolling_12mo = []


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

    time_stats = build_time_stats()
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

    compute_user_time_stats(message)


def compute_user_time_stats(message):
    create_time = message.get("create_time")
    if create_time is None:
        return

    try:
        sent_dt_utc = datetime.fromtimestamp(float(create_time), tz=timezone.utc)
    except (TypeError, ValueError, OSError):
        return

    hour_label = format_hour_label(sent_dt_utc.hour)
    day_label = sent_dt_utc.strftime("%A")
    month_label = sent_dt_utc.strftime("%B")
    year_label = str(sent_dt_utc.year)
    date_label = sent_dt_utc.date().isoformat()

    msgs_sent_by_hour[hour_label] = msgs_sent_by_hour.get(hour_label, 0) + 1
    msgs_sent_by_day[day_label] = msgs_sent_by_day.get(day_label, 0) + 1
    msgs_sent_by_month[month_label] = msgs_sent_by_month.get(month_label, 0) + 1
    msgs_sent_by_year[year_label] = msgs_sent_by_year.get(year_label, 0) + 1
    msgs_sent_by_date[date_label] = msgs_sent_by_date.get(date_label, 0) + 1


def format_hour_label(hour):
    if hour == 0:
        return "12 AM"
    if hour < 12:
        return f"{hour} AM"
    if hour == 12:
        return "12 PM"
    return f"{hour - 12} PM"


def build_time_stats():
    global msgs_sent_rolling_12mo
    msgs_sent_rolling_12mo = compute_rolling_time_stats()

    return {
        "msgs_sent_by_hour": msgs_sent_by_hour,
        "msgs_sent_by_day": msgs_sent_by_day,
        "msgs_sent_by_month": msgs_sent_by_month,
        "msgs_sent_by_year": msgs_sent_by_year,
        "msgs_sent_rolling_12mo": msgs_sent_rolling_12mo,
    }


def compute_rolling_time_stats():
    if not msgs_sent_by_date:
        return []

    latest_date = max(datetime.strptime(date, "%Y-%m-%d").date() for date in msgs_sent_by_date)
    start_date = latest_date - timedelta(days=364)

    rolling_stats = []
    current_date = start_date
    while current_date <= latest_date:
        date_label = current_date.isoformat()
        rolling_stats.append(
            {
                "date": date_label,
                "count": msgs_sent_by_date.get(date_label, 0),
            }
        )
        current_date += timedelta(days=1)

    return rolling_stats


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
