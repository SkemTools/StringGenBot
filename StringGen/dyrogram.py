from config import ( BOT_TOKEN, API_ID, API_HASH ) 

from pyrogram import Client
from pyromod import listen

app = Client(
    "wbb",
    bot_token=BOT_TOKEN,
    api_id=API_ID,
    api_hash=API_HASH
)

