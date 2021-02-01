"""
    Initialize database structure
"""
import json
from sqlalchemy import create_engine, Column, Integer, String, Date, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import DATABASE_URL

Base = declarative_base()

engine = create_engine(DATABASE_URL, echo=False, pool_size=20, max_overflow=0)
Session = sessionmaker(bind=engine)


class Reminder(Base):
    __tablename__ = 'reminders'
    reminder_id = Column(Integer, primary_key=True)
    name = Column(String)
    birth_date = Column(Date)
    age = Column(Integer)
    remind_date = Column(Date)
    owner_id = Column(Integer)
    owner_username = Column(String)
    owner_first_name = Column(String)
    owner_last_name = Column(String)
    datetime_added = Column(DateTime)


# Use this to create initial database structure
Base.metadata.create_all(engine)
