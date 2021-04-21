from pyrogram import Client,filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from StringGen.filters import command, other_filters, other_filters2
from StringGen import devil as app

@app.on_message(command("start") & other_filters2)
async def start(_, message: Message):
    await message.reply_text(
        f"""🙃 Hi {message.from_user.first_name}!
✨ Hey I am DaisyX String Generator Bot. 
🥳 I can Generator String Session for You 😉
⚜️ Use these buttons below to know more. 👇
🔥 Source Code Made by Devil With Help Of Other Bots 🔥
👉 Type /genstr for Generating String Session 👈""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "⚒ Source code", url="https://github.com/SkemTools"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "💬 Group", url="https://t.me/DaisySupport_Official"
                    ),
                    InlineKeyboardButton(
                        "Channel 🔈", url="https://t.me/DaisyXUpdates"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "❌ Close ❌", callback_data="close"
                    )
                ]
            ]
        )
    )


