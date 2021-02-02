"""
    Handler that shows the reminders of a given user
"""

import logging
from telegram.ext import CommandHandler
from jobs.db_ops import get_reminders
from datetime import date

logger = logging.getLogger(__name__)


def select_reminders(chat_id):
    today = date.today()
    reminders = get_reminders(order_attr='remind_date', owner_id=chat_id)
    result = {}
    for record in reminders:
        remind_id = record.reminder_id
        remind_date = record.remind_date.strftime("%d.%m")
        name = record.name
        age = record.age
        days_till_bd = (record.remind_date-today).days
        record_object = {remind_id: {'remind_date': remind_date,
                                     'name': name,
                                     'age': age,
                                     'days_till_bd': days_till_bd}}
        result.update(record_object)
    return result


def print_reminders(update, context):
    chat = update.message.chat.id
    msg = ''
    reminders = select_reminders(chat)
    for k, v in reminders.items():
        msg += f"{v['remind_date']} (days left: {v['days_till_bd']}) | {v['name']} | age: {v['age']} *(id:{k})*\n"
    if msg:
        update.message.reply_text(f'*📆 List of reminders*\n{msg}', parse_mode='markdown')
    else:
        update.message.reply_text('No reminders set yet')
    logger.info('Reminders shown')


list_reminders = CommandHandler('list', print_reminders)
