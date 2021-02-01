"""
    Handler that manages reminders removal
"""
import logging
from telegram.ext import ConversationHandler, CallbackQueryHandler, CommandHandler, MessageHandler, Filters
from handlers.misc import cancel, cancel_keyboard
from jobs.db_ops import remove_reminder

logger = logging.getLogger(__name__)

# --- states use in conversation ---
READ_DELETE = 100


def rm_reminder(update, context):
    logger.info("STARTED new reminder removal")
    if not context.args:
        update.effective_message.reply_text("🗑 What reminder do you want to delete?"
                                            " (use id to delete reminder)", quote=False, reply_markup=cancel_keyboard())
        logger.info("Waiting user input on what reminder to remove..")
        return READ_DELETE
    reminder_key = ' '.join(context.args)
    return _delete_reminder(update, reminder_key)


def rm_reminder_from_text(update, context):
    reminder_key = update.message.text
    return _delete_reminder(update, reminder_key)


def _delete_reminder(update, reminder_key):
    msg = remove_reminder(
        reminder_id=reminder_key,
        owner_id=str(update.message.from_user.id),
    )
    update.message.reply_text(msg, parse_mode='markdown')

    logger.info("ENDED reminder removal successfully")
    return ConversationHandler.END


remove_reminders = ConversationHandler(
    entry_points=[CommandHandler('delete', rm_reminder)],
    states={
        READ_DELETE: [
            CallbackQueryHandler(cancel, pattern='^/cancel$'),
            # has to be before MessageHandler to catch `/cancel` as command, not as `name`
            MessageHandler(Filters.text, rm_reminder_from_text)
        ],
    },
    fallbacks=[CallbackQueryHandler(cancel, pattern='^/cancel$')],
)
