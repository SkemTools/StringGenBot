import asyncio
import re
import importlib
import uvloop
from pyrogram import filters, idle
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from StringGen.dyrogram import devil as app
from StringGen.StringGenerator import ALL_MODULES
from math import ceil
from pyrogram.types import InlineKeyboardButton



loop = asyncio.get_event_loop()

HELPABLE = {}


class EqInlineKeyboardButton(InlineKeyboardButton):
    def __eq__(self, other):
        return self.text == other.text

    def __lt__(self, other):
        return self.text < other.text

    def __gt__(self, other):
        return self.text > other.text


def paginate_modules(page_n, module_dict, prefix, chat=None):
    if not chat:
        modules = sorted(
            [
                EqInlineKeyboardButton(
                    x.__MODULE__,
                    callback_data="{}_module({})".format(
                        prefix, x.__MODULE__.lower()),
                )
                for x in module_dict.values()
            ]
        )
    else:
        modules = sorted(
            [
                EqInlineKeyboardButton(
                    x.__MODULE__,
                    callback_data="{}_module({},{})".format(
                        prefix, chat, x.__MODULE__.lower()
                    ),
                )
                for x in module_dict.values()
            ]
        )

    pairs = list(zip(modules[::3], modules[1::3], modules[2::3]))
    i = 0
    for m in pairs:
        for _ in m:
            i += 1
    if len(modules) - i == 1:
        pairs.append((modules[-1],))
    elif len(modules) - i == 2:
        pairs.append(
            (
                modules[-2],
                modules[-1],
            )
        )

    max_num_pages = ceil(len(pairs) / 7)
    modulo_page = page_n % max_num_pages

    # can only have a certain amount of buttons side by side
    if len(pairs) > 7:
        pairs = pairs[modulo_page * 7: 7 * (modulo_page + 1)] + [
            (
                EqInlineKeyboardButton(
                    "<",
                    callback_data="{}_prev({})".format(
                        prefix, modulo_page
                    ),
                ),
                EqInlineKeyboardButton(
                    ">",
                    callback_data="{}_next({})".format(
                        prefix, modulo_page
                    ),
                ),
            )
        ]

    return pairs




async def start_bot():
    global COMMANDS_COUNT
    for module in ALL_MODULES:
        imported_module = importlib.import_module("StringGen.StringGenerator." + module)
        if (
            hasattr(imported_module, "__MODULE__")
            and imported_module.__MODULE__
        ):
            imported_module.__MODULE__ = imported_module.__MODULE__
            if (
                hasattr(imported_module, "__HELP__")
                and imported_module.__HELP__
            ):
                HELPABLE[
                    imported_module.__MODULE__.lower()
                ] = imported_module
    bot_modules = ""
    j = 1
    for i in ALL_MODULES:
        if j == 4:
            bot_modules += "|{:<15}|\n".format(i)
            j = 0
        else:
            bot_modules += "|{:<15}".format(i)
        j += 1
    print("+===============================================================+")
    print("|                         Devil - Modules                         |")
    print("+===============+===============+===============+===============+")
    print(bot_modules)
    print("+===============+===============+===============+===============+")
    print(f"BOT Started Successfully as DaisyXScrapper!")
    print(f"BOT Started Successfully as DaisyXScrapper!")
    await idle()


@app.on_message(filters.command(["help", "start"]))
async def help_command(_, message):
    if message.chat.type != "private":
        if len(message.command) >= 2 and message.command[1] == "help":
            text, keyboard = await help_parser(message)
            await message.reply(
                text, reply_markup=keyboard, disable_web_page_preview=True
            )
            return
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="Help ❓",
                        url=f"t.me/DaisyXScrapperBot?start=help",
                    ),
                    InlineKeyboardButton(
                        text="Repo 🛠",
                        url="https://github.com/SkemTools",
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="System Stats 💻",
                        callback_data="stats_callback"
                    ),
                    InlineKeyboardButton(
                        text="Support 👨",
                        url="t.me/DaisySupport_Official"
                    )
                ]
            ]
        )
        await message.reply("Pm Me For More Details.", reply_markup=keyboard)
        return
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="Commands ❓",
                    callback_data="bot_commands"
                ),
                InlineKeyboardButton(
                    text="Repo 🛠",
                    url="https://github.com/SkemTools"
                )
            ],
            [
                InlineKeyboardButton(
                    text="Developer 🖥",
                    url="t.me/lucifeermorningstar"
                ),
                InlineKeyboardButton(
                    text="Support 👨",
                    url="t.me/DaisySupport_Official"
                )
            ],
            [
                InlineKeyboardButton(
                    text="Add Me To Your Group 🎉",
                    url=f"http://t.me/DaisyXScrapperBot?startgroup=new"
                )
            ]
        ]
    )
    await message.reply(f"Hey there! My name is {BOT_NAME}. I can manage your group with lots of useful features, feel free to add me to your group.", reply_markup=keyboard)


async def help_parser(name, keyboard=None):
    if not keyboard:
        keyboard = InlineKeyboardMarkup(paginate_modules(0, HELPABLE, "help"))
    return (
        """Hello {first_name}! My name is {bot_name}!
I'm a group management bot with some usefule features.
You can choose an option below, by clicking a button.
Also you can ask anything in Support Group.

General command are:
 - /start: Start the bot
 - /help: Give this message""".format(
            first_name=name,
            bot_name=BOT_NAME,
        ),
        keyboard,
    )


@app.on_callback_query(filters.regex("bot_commands"))
async def commands_callbacc(_, CallbackQuery):
    text, keyboard = await help_parser(CallbackQuery.from_user.mention)
    await app.send_message(
        CallbackQuery.message.chat.id,
        text=text,
        reply_markup=keyboard
    )

    await CallbackQuery.message.delete()


@app.on_callback_query(filters.regex(r"help_(.*?)"))
async def help_button(client, query):
    mod_match = re.match(r"help_module\((.+?)\)", query.data)
    prev_match = re.match(r"help_prev\((.+?)\)", query.data)
    next_match = re.match(r"help_next\((.+?)\)", query.data)
    back_match = re.match(r"help_back", query.data)
    create_match = re.match(r"help_create", query.data)

    if mod_match:
        module = mod_match.group(1)
        text = (
            "{} **{}**:\n".format(
                "Here is the help for", HELPABLE[module].__MODULE__
            )
            + HELPABLE[module].__HELP__
        )

        await query.message.edit(
            text=text,
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("back", callback_data="help_back")]]
            ),
            disable_web_page_preview=True,
        )

    elif prev_match:
        curr_page = int(prev_match.group(1))
        await query.message.edit(
            text="Hi {first_name}. I am {bot_name}".format(
                first_name=query.from_user.first_name,
                bot_name=BOT_NAME,
            ),
            reply_markup=InlineKeyboardMarkup(
                paginate_modules(curr_page - 1, HELPABLE, "help")
            ),
            disable_web_page_preview=True,
        )

    elif next_match:
        next_page = int(next_match.group(1))
        await query.message.edit(
            text="Hi {first_name}. I am {bot_name}".format(
                first_name=query.from_user.first_name,
                bot_name=BOT_NAME,
            ),
            reply_markup=InlineKeyboardMarkup(
                paginate_modules(next_page + 1, HELPABLE, "help")
            ),
            disable_web_page_preview=True,
        )

    elif back_match:
        await query.message.edit(
            text="Hi {first_name}. I am {bot_name}".format(
                first_name=query.from_user.first_name,
                bot_name=BOT_NAME,
            ),
            reply_markup=InlineKeyboardMarkup(
                paginate_modules(0, HELPABLE, "help")
            ),
            disable_web_page_preview=True,
        )

    elif create_match:
        text, keyboard = await help_parser(query)
        await query.message.edit(
            text=text, reply_markup=keyboard, disable_web_page_preview=True
        )

    return await client.answer_callback_query(query.id)


if __name__ == "__main__":
    uvloop.install()
    loop.run_until_complete(start_bot())
