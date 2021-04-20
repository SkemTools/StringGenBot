# © Copyright 2021 - 2022 TeamDaisyX
# All Credit For This File Goes to Team DaisyX. 
# Ported Here By Devil. 


from pyrogram import Client, errors

from StringGen.config import get_str_key, get_int_key

TOKEN = get_str_key("TOKEN", required=True)
APP_ID = get_int_key("APP_ID", required=True)
APP_HASH = get_str_key("APP_HASH", required=True)
session_name = TOKEN.split(':')[0]
pbot = Client(session_name, api_id=APP_ID, api_hash=APP_HASH, bot_token=TOKEN)

