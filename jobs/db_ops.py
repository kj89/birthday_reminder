"""
    Handle operations with database
"""
import logging
from jobs.models import Session, Reminder

logger = logging.getLogger(__name__)


def add_reminder(reminder):
    session = Session()
    session.add(reminder)
    session.commit()


def remove_reminder(reminder_id, **kwargs):
    session = Session()
    try:
        reminder = session.query(Reminder).filter_by(reminder_id=reminder_id, **kwargs).first()
        if reminder is None:
            logger.info(f"Reminder {reminder_id} does not exist on db")
            msg = f'🚫 Reminder `{reminder_id}` does not exist in database'
        else:
            session.delete(reminder)
            logger.info(f"Reminder {reminder_id!r} DELETED")
            msg = f'✅ Reminder `{reminder_id}` deleted successfully!'
    except Exception:
        logger.info(f"Error {reminder_id} running query")
        msg = f'🚫 Please check if reminder id: {reminder_id!r} is correct!'

    session.commit()
    return msg


def get_reminders(order_attr=None, **kwargs):
    session = Session()
    query = session.query(Reminder).filter_by(**kwargs).order_by(order_attr)
    return query


def update_reminders(reminder_id):
    session = Session()
    reminder = session.query(Reminder).filter_by(reminder_id=reminder_id).first()
    n_remind_date = reminder.remind_date.replace(year=reminder.remind_date.year + 1)
    reminder.remind_date = n_remind_date
    reminder.age += 1
    session.commit()


def get_all_chats():
    session = Session()
    records = session.query(Reminder.owner_id).distinct().all()
    values = [record[0] if len(record) == 1 else record for record in records]
    return values
