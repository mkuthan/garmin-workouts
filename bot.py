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
import os
import datetime
from dateutil import tz

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
    planning: dict = configreader.read_config(os.path.join('.', 'events', 'planning', 'planning.yaml'))

    keyboard: list[list[InlineKeyboardButton]] = []
    keyboard.append([InlineKeyboardButton('Zones', callback_data='Zones')])
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
        cmd: str = str("python -m garminworkouts event-import Races")
    elif workout == 'Zones':
        cmd: str = str("python -m garminworkouts user-zones")
    else:
        cmd = str("python -m garminworkouts trainingplan-import ") + workout

    subprocess.run(cmd, shell=True, capture_output=True)

    with open('./debug.log', 'r') as file:
        assert query.message is not None
        await query.message.reply_text(text=file.read())


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Displays info on how to use the bot."""
    assert update.message is not None
    await update.message.reply_text("Use /start to test this bot.")


async def recurrent(context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = next(iter(context.application._chat_ids_to_be_updated_in_persistence))
    await context.bot.send_message(chat_id, text='Daily trainingplan update')
    planning: dict = configreader.read_config(os.path.join('.', 'events', 'planning', 'planning.yaml'))

    for plan in planning:
        await context.bot.send_message(chat_id, text='Updating ' + plan)
        if plan != 'Races':
            cmd: str = str("python -m garminworkouts trainingplan-import " + plan)
        else:
            cmd: str = str("python -m garminworkouts event-import Races")

        subprocess.run(cmd, shell=True, capture_output=True)

        with open('./debug.log', 'r') as file:
            await context.bot.send_message(chat_id, text=file.read())


def remove_job_if_exists(name: str, context: ContextTypes.DEFAULT_TYPE) -> bool:
    """Remove job with given name. Returns whether job was removed."""
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True


async def set_timer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Add a job to the queue."""
    chat_id = update.effective_message.chat_id
    try:
        job_removed = remove_job_if_exists(str(chat_id), context)
        context.job_queue.run_daily(callback=recurrent,
                                    time=datetime.time(hour=3, minute=00, second=00,
                                                       tzinfo=tz.gettz('Europe/Madrid')))

        text = "Recurrent workout update successfully set!"
        if job_removed:
            text += " Old one was removed."
        await update.effective_message.reply_text(text)

    except (IndexError, ValueError):
        await update.effective_message.reply_text("Usage: Recurrent workout update")


async def unset(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Remove the job if the user changed their mind."""
    chat_id = update.message.chat_id
    job_removed = remove_job_if_exists(str(chat_id), context)
    text = "Recurrent task successfully cancelled!" if job_removed else "You have no active timer."
    await update.message.reply_text(text)


def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(account.BOT_TOKEN).build()  # type: ignore

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("set", set_timer))
    application.add_handler(CommandHandler("unset", unset))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    with contextlib.suppress(KeyboardInterrupt):  # Ignore exception when Ctrl-C is pressed
        assert main() is not None
        asyncio.run(main())  # type: ignore
