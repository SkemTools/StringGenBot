from pyrogram import Client
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from StringGen.filters import command, other_filters, other_filters2


@Client.on_message(command("start") & other_filters2)
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
                        "⚒ Channel code", url="https://t.me/Abo_Hadieda"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "DEV", url="https://t.me/Abu_hadieda"
                    ),
                    InlineKeyboardButton(
                        "Channel 🔈", url="https://t.me/Abo_Hadieda"
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


