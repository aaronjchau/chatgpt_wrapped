# from fastapi import APIRouter, HTTPException, UploadFile
from pprint import pprint
from app.services import parser, stats

# router = APIRouter()


# # route to import conversations.json and generate stats and plots
# @router.post("/upload")
# async def upload(file: UploadFile):


# read in my json conversations
data = parser.load_conversations()

# compute a list of dicts, with 1 dict for each message
all_messages = parser.parse(data)

global_stats, conversation_stats, model_stats = stats.compute_stats(all_messages)

pprint(global_stats)
print()
# pprint(conversation_stats)
# print()
pprint(model_stats)
print()