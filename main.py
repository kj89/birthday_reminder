#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Simple Bot to remind about upcoming birthdays
"""

import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from handlers.misc import start, error, ups_handler, default, commands
from handlers.notifications import start_all_notify, start_notify, stop_notify, get_status_notify
from handlers.delete import remove_reminders
from handlers.list import list_reminders
from handlers.add import add_reminders
from jobs.db_ops import get_all_chats
from config import TOKEN

# --- structure for data ---
data = {'name': "", 'date': ""}

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(TOKEN)

    # Start notifications on all chats and set notification time
    chat_list = get_all_chats()
    if chat_list:
        start_all_notify(updater, get_all_chats())

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Define handlers
    start_handler = CommandHandler('start', start)
    start_notifications = CommandHandler('notify_start', start_notify)
    stop_notifications = CommandHandler('notify_stop', stop_notify)
    status_notifications = CommandHandler('notify_status', get_status_notify)
    info_handler = CommandHandler('commands', commands)
    fallback_handler = MessageHandler(Filters.all, default)

    # Use bot handlers
    dp.add_handler(start_handler)
    dp.add_handler(start_notifications)
    dp.add_handler(stop_notifications)
    dp.add_handler(status_notifications)
    dp.add_handler(info_handler)
    dp.add_handler(add_reminders)
    dp.add_handler(remove_reminders)
    dp.add_handler(list_reminders)

    # Add special handlers. Error handler and fallback handler.
    dp.add_error_handler(ups_handler)
    dp.add_handler(fallback_handler)

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
