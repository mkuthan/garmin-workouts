#!/usr/bin/env python
# pylint: disable=wrong-import-position
# pylance: reportOptionalMemberAccess=false
"""Simple Bot to reply to Telegram messages.

This is built on the API wrapper, see echobot.py to see the same example built
on the telegram.ext bot framework.
This program is dedicated to the public domain under the CC0 license.
"""
import subprocess

import asyncio
import contextlib
import logging
import account

from telegram import __version__ as TG_VER
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes

from garminworkouts.config import configreader
try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )


class Arg(object):
    def __init__(
        self,
        workout,
        cookie_jar,
        connect_url,
        sso_url
    ) -> None:
        self.workout: tuple = workout,
        self.cookie_jar: tuple = cookie_jar,
        self.connect_url: tuple = connect_url,
        self.sso_url: tuple = sso_url,


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a message with three inline buttons attached."""
    planning: dict = configreader.read_config(r'./events/planning/planning.yaml')

    keyboard: list[list[InlineKeyboardButton]] = [
        [
            InlineKeyboardButton("Option 1", callback_data="1"),
            InlineKeyboardButton("Option 2", callback_data="2"),
        ],
        [InlineKeyboardButton("Workout import", callback_data="3")],
    ]

    keyboard = []
    for key in planning.keys():
        keyboard.append([InlineKeyboardButton(key, callback_data=key)])

    reply_markup = InlineKeyboardMarkup(keyboard)

    assert update.message is not None
    await update.message.reply_text("Please choose:", reply_markup=reply_markup)


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    assert query is not None
    await query.answer()

    workout = str(query.data)
    await query.edit_message_text(text=f"Selected option: {query.data}")

    if workout == 'Races':
        cmd: str = str("python -m garminworkouts import-event ") + workout
    else:
        cmd = str("python -m garminworkouts import-workout ") + workout

    returned_value = subprocess.run(cmd, shell=True, capture_output=True)

    output: str = f'{str(returned_value)}\n'

    with open('./debug.log', 'r') as file:
        output: str = output + file.read()

    assert query.message is not None
    await query.message.reply_text(text=output)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Displays info on how to use the bot."""
    assert update.message is not None
    await update.message.reply_text("Use /start to test this bot.")


def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(account.BOT_TOKEN).build()  # type: ignore

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(CommandHandler("help", help_command))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    with contextlib.suppress(KeyboardInterrupt):  # Ignore exception when Ctrl-C is pressed
        assert main() is not None
        asyncio.run(main())  # type: ignore
