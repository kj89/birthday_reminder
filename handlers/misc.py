import logging
from datetime import date, datetime
from telegram import TelegramError
from telegram.ext import ConversationHandler
from telegram import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from config import BOT_USERNAME, NOTIFICATION_DAYS, NOTIFICATION_TIME

logger = logging.getLogger(__name__)


def start(update, context):
    """Send message on `/start`."""
    # Get user that sent /start and log his name
    user = update.message.from_user
    notify_days = ", ".join([str(el) for el in NOTIFICATION_DAYS])
    kb = [[KeyboardButton('/add'), KeyboardButton('/delete')],
          [KeyboardButton('/list')]]
    kb_markup = ReplyKeyboardMarkup(kb, one_time_keyboard=False, resize_keyboard=True)
    update.message.reply_text(f"Hi {user.first_name} and welcome to @{BOT_USERNAME}!\n"
                              f"I will remind you about birthdays of your family and friends. By default the bot "
                              f"will remind you an important date several times - <b>{notify_days}</b> days before, "
                              f"<b>1</b> day before and <b>on the day</b> itself at <b>{NOTIFICATION_TIME}:00</b>. "
                              f"Please use keyboard buttons below to interact with me or use /commands to show "
                              f"list of available commands",
                              reply_markup=kb_markup, parse_mode='html')
    logger.info("User %s started the conversation.", user.first_name)


def commands(update, context):
    """Send user information about available commands ad descriptions"""
    context.bot.send_message(
        chat_id=update.effective_message.chat_id,
        text="Available commands:\n"
             "/start - initialize bot\n"
             "/add - add reminder to database\n"
             "/delete - remove reminder from database\n"
             "/list - show list of reminders saved in database\n"
             "/notify_start - turn on notifications\n"
             "/notify_stop - turn off notifications\n"
             "/notify_status - get current notification status"
    )


def ups_handler(update, context):
    try:
        raise context.error
    except TelegramError:
        logger.exception("A Telegram error occurred")
    except Exception:
        logger.exception("A general error occurred")
    finally:
        update.effective_message.reply_text(f'Errors happen ¯\\_(ツ)_/¯')


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def default(update, context):
    """If a user sends an unknown command, answer accordingly"""
    context.bot.send_message(
        chat_id=update.effective_message.chat_id,
        text="I don't get you 🧐\n"
             "Please write /start to start the bot"
    )


def cancel(update, context):
    """Returns `ConversationHandler.END`, which tells the
    ConversationHandler that the conversation is over"""
    query = update.callback_query
    query.answer()
    query.edit_message_text(text="Canceled!")
    return ConversationHandler.END


def cancel_keyboard():
    keyboard = [[InlineKeyboardButton('cancel', callback_data='/cancel')]]
    return InlineKeyboardMarkup(keyboard)


def str_to_date(event_date):
    today = date.today()
    year = event_date.split(".")[-1]
    if len(year) == 2:
        event_date = datetime.strptime(event_date, '%d.%m.%y').strftime('%d.%m.%Y')
    dd, mm, yyyy = [int(x) for x in event_date.split('.')]
    result_date = date(yyyy, mm, dd)
    if today.year < result_date.year:
        modifier = 100
    else:
        modifier = 0
    result_date = result_date.replace(year=result_date.year - modifier)
    return result_date


def get_age(event_date):
    today = date.today()
    age = today.year - event_date.year + ((today.month, today.day) > (event_date.month, event_date.day))
    return age


def get_reminder_date(event_date):
    today = date.today()
    result_date = event_date.replace(year=today.year + ((today.month, today.day) > (event_date.month, event_date.day)))
    return result_date
