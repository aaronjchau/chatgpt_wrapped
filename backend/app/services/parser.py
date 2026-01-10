from pprint import pprint
import json

JSON_PATH = "tests/fixtures/conversations_small.json"


def load_conversations():
    with open(JSON_PATH, "r", encoding="utf-8") as handle:
        return json.load(handle)


def parse(json_data):

    # use a list of dicts, with 1 dict for each message in a conversation
    all_messages_props = []

    for conversation in json_data:

        # store conversation ID so we can calculate # of convos 
        convo_id = conversation["id"]

        # iterate thru all messages in each chat
        for node in conversation["mapping"].values():
            message = {}

            # skip unrelated nodes
            if node.get("message") is None:
                continue

            role = node["message"]["author"]["role"]
            message_list = node["message"]["content"].get("parts")
            if not message_list: 
                continue
            model_id = node["message"]["metadata"].get("model_slug")

            # NOTE: parts is a list that includes the string message and dicts if images are attached
            message_list_strings = [s for s in message_list if isinstance(s, str)]
            text = message_list_strings[0] if message_list_strings else ""

            message["conversation_id"] = convo_id
            message["role"] = role
            message["text"] = text 
            message["model_id"] = model_id

            all_messages_props.append(message)

    return all_messages_props