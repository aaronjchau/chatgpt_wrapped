from pprint import pprint
import json

JSON_PATH = "backend/tests/fixtures/conversations_small.json"


def load_conversations():
    with open(JSON_PATH, "r", encoding="utf-8") as handle:
        return json.load(handle)


data = load_conversations()

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

# iterate thru all chats
for conversation in data:
    # include conversation in global count
    global_stats["total_convos"] += 1

    convo_id = conversation["id"]


    # temporarily store the title to reference for spot checks
    if convo_id not in conversation_stats:
        conversation_stats[convo_id] = {
            "convo_msgs_sent": 0,
            "convo_words_sent": 0,
            "convo_msgs_recd": 0,
            "convo_words_recd": 0,
            "title": conversation["title"],
        }

    # iterate thru all messages in each chat
    for node in conversation["mapping"].values():

        if node.get("message") is None:
            continue

        role = node["message"]["author"]["role"]
        message_list = node["message"]["content"].get("parts")

        # make sure this is a valid sent message
        if role == "user" and message_list is not None:
            # count message sent for this convo
            conversation_stats[convo_id]["convo_msgs_sent"] += 1

            # NOTE: parts is a list that includes the string message and dicts if images are attached
            message_list_strings = [s for s in message_list if isinstance(s, str)]

            # guard for case where there are only images attached and no message
            message = message_list_strings[0] if message_list_strings else ""

            # count words in this message sent
            conversation_stats[convo_id]["convo_words_sent"] += len(message.split())

            # include message sent count in global count
            global_stats["total_msgs_sent"] += 1

            # include word count in global count
            global_stats["total_words_sent"] += len(message.split())

        # make sure this is a valid received message
        if role == "assistant" and message_list is not None:

            message_list_strings = [s for s in message_list if isinstance(s, str)]

            message = message_list_strings[0] if message_list_strings else ""


            # if there's no message, don't include it because chatGPT always responds at least some text
            if not message:
                continue
            
            # if there's no model id, it probably was a regenerated message so skip it 
            model_id = node["message"]["metadata"].get("model_slug")
            if not model_id: 
                continue

            if model_id not in model_stats:
                model_stats[model_id] = 0

            # include message received in tally by AI model
            model_stats[model_id] += 1

            conversation_stats[convo_id]["convo_msgs_recd"] += 1

            conversation_stats[convo_id]["convo_words_recd"] += len(message.split())

            global_stats["total_msgs_recd"] += 1

            global_stats["total_words_recd"] += len(message.split())

pprint(global_stats)
print()
pprint(conversation_stats)
print()
pprint(model_stats)
