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


# compute stats for all messages
def compute_stats(all_messages_props):
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
    
    return global_stats, conversation_stats, model_stats


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