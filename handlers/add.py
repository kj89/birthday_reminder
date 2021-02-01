"""
    Handler that manages creation of new reminders
"""
import logging
from telegram.ext import ConversationHandler, CommandHandler, MessageHandler, CallbackQueryHandler, Filters
from handlers.misc import cancel, cancel_keyboard, str_to_date, get_age, get_reminder_date
from jobs.db_ops import add_reminder
from jobs.models import Reminder
from datetime import datetime

# --- states use in conversation ---
READ_NAME = 1
READ_DATE = 2

logger = logging.getLogger(__name__)


def add(update, context):
    global data  # to assign new dictionary to external/global variable
    data = {'name': "", 'date': ""}
    update.message.reply_text("Input reminder name", reply_markup=cancel_keyboard())
    return READ_NAME


def get_add_name(update, context):
    data['name'] = update.message.text
    update.message.reply_text(f"Input reminder date. For example 30.12.1990 or 1.1.89", reply_markup=cancel_keyboard())
    return READ_DATE


def get_add_date(update, context):
    try:
        data['date'] = str_to_date(update.message.text)
    except ValueError as error_msg:
        update.message.reply_text(f'Invalid format. Try again.')
        return
    else:
        add_reminder_to_db(update, context)
        msg = f"*{data['name']}* successfully added to db!"
        update.message.reply_text(msg, parse_mode='Markdown')
        return ConversationHandler.END


def add_reminder_to_db(update, context):
    """Saves a reminder in db based on the update"""
    try:
        reminder = Reminder(
            name=data['name'],
            birth_date=data['date'],
            age=get_age(data['date']),
            remind_date=get_reminder_date(data['date']),
            owner_id=update.message.chat.id,
            owner_username=update.message.chat.username,
            owner_first_name=update.message.chat.first_name,
            owner_last_name=update.message.chat.last_name,
            datetime_added=datetime.today()
        )
        add_reminder(reminder)
        return True
    except KeyError:
        logger.exception('Job context keys not properly initialized.')
        return False
    except Exception:
        logger.exception("Error saving reminder to db.")
        return False


add_reminders = ConversationHandler(
    entry_points=[CommandHandler('add', add)],
    states={
        READ_NAME: [
            CallbackQueryHandler(cancel, pattern='^/cancel$'),
            # has to be before MessageHandler to catch `/cancel` as command, not as `name`
            MessageHandler(Filters.text, get_add_name)
        ],
        READ_DATE: [
            CallbackQueryHandler(cancel, pattern='^/cancel$'),
            # has to be before MessageHandler to catch `/cancel` as command, not as `name`
            MessageHandler(Filters.text, get_add_date)
        ],
    },
    fallbacks=[CallbackQueryHandler(cancel, pattern='^/cancel$')],
)
