import logging
from datetime import time, datetime
import pytz
from handlers.list import select_reminders
from jobs.db_ops import update_reminders
from config import NOTIFICATION_TIME, NOTIFICATION_DAYS

logger = logging.getLogger(__name__)


def set_notification_time():
    d = datetime.now()
    timezone = pytz.timezone("Europe/Riga")
    d_aware = timezone.localize(d)
    notify_time = time(NOTIFICATION_TIME, 0, 0, 0, tzinfo=d_aware.tzinfo)
    return notify_time


def start_notify(update, context):
    jobs = context.job_queue
    chat = update.message.chat_id
    notify_time = set_notification_time()
    job_count = jobs.get_jobs_by_name(f'daily {str(chat)}')  # This will return a tuple of jobs
    if not job_count:
        context.bot.send_message(chat_id=chat, text='Starting notifications...')
        jobs.run_daily(send_notify, notify_time, context=update.message.chat_id, name=f'daily {str(chat)}')
    else:
        context.bot.send_message(chat_id=chat, text='Notifications are already started!')


def stop_notify(update, context):
    jobs = context.job_queue
    chat = update.message.chat_id
    job_list = jobs.get_jobs_by_name(f'daily {str(chat)}')  # This will return a tuple of jobs
    if len(job_list):
        context.bot.send_message(chat_id=chat, text='Stopping notifications...')
        job_list[0].schedule_removal()  # It will be removed without executing its callback function again
    else:
        context.bot.send_message(chat_id=chat, text=f'Notifications are already stopped!')


def get_status_notify(update, context):
    jobs = context.job_queue
    chat = update.message.chat_id
    job_list = jobs.get_jobs_by_name(f'daily {str(chat)}')  # This will return a tuple of jobs
    if len(job_list):
        context.bot.send_message(chat_id=chat, text='🟢 Notifications ON!')
    else:
        context.bot.send_message(chat_id=chat, text='🔴 Notifications OFF!')


def send_notify(context):
    chat = context.job.context
    reminders = select_reminders(chat)
    msg = ''
    for k, v in reminders.items():
        days_till_bd = v['days_till_bd']
        name = v['name']
        age = v['age']
        if days_till_bd in NOTIFICATION_DAYS:
            msg += f"🍉 *{name}* turns *{age}* in *{days_till_bd}* days!\n"
        if days_till_bd == 1:
            msg += f"🦄 Tomorrow *{name}* turns *{age}*!\n"
        if days_till_bd == 0:
            msg += f"🥳 Hooray! Today *{name}* calebrates his/her *{age}* birthday!\n"
            update_reminders(k)
        if days_till_bd < 0:
            update_reminders(k)
    if msg:
        context.bot.send_message(chat_id=chat, text=msg, parse_mode='markdown')
        logger.info('Notifications sent')


def start_all_notify(context, chats):
    jobs = context.job_queue
    notify_time = set_notification_time()
    for chat in chats:
        # jobs.run_repeating(send_notify, interval=10.0, context=chat, name=f'daily {str(chat)}') # for testing
        jobs.run_daily(send_notify, notify_time, context=chat, name=f'daily {str(chat)}')
