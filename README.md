# Birthday reminder bot
 This bot reminds you about birthdays of your family and friends.

By default the bot will remind you an important date several times - ___14, 7___ days before, ___1___ day before and ___on the day___ itself at ___10 AM___
Configuration for notifications can be set in `config.py` file

## How to start
1. Clone this repository
2. Install ___postgresql___ and create _new database_
3. Get you telegram bot ___API token___
4. Manage configuration in `config.py` file
5. Open project and run `main.py`

## Prerequisites
For this specific project I used python version ___3.8.2___
Python packages used for this project (latest available versions in the time when bot was written) :
* `pytz 2020.5` - this library is used to get accurate timezone
* `python-telegram-bot 13.1` - this library provides a pure Python interface for the [Telegram Bot API](https://core.telegram.org/bots/api)
* `sqlalchemy 1.3.22` - to store and manage data in _postgresql_ database
 
## Bot commands
`/start` - _initialize bot_
\
`/add` - _add reminder to database_
\
`/delete` - _remove reminder from database_
\
`/list` - _show list of reminders saved in database_
\
`/notify_start` - _turn on notifications_
\
`/notify_stop` - _turn off notifications_
\
`/notify_status` - _get current notification status_