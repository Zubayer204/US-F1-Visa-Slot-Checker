from os import getenv
from calendar import month_name
import re
import sqlite3
import emails
import pytz
from dotenv import load_dotenv
from telethon import TelegramClient, events
import datetime as dt


# get app credentials
load_dotenv()
api_id = int(getenv('API_ID'))
api_hash = getenv('API_HASH')
SMTP_USER = getenv("SMTP_USER")
SMTP_PASS = getenv("SMTP_PASS")

# connect to database
conn = sqlite3.connect("database.db", detect_types=sqlite3.PARSE_DECLTYPES)
cursor = conn.cursor()
cursor.execute(
    '''CREATE TABLE IF NOT EXISTS alarms (id INTEGER PRIMARY KEY, email TEXT UNIQUE, notif_date DATE)''')
cursor.execute(
    '''CREATE TABLE IF NOT EXISTS data (id INTEGER PRIMARY KEY, slot_date DATE, updated DATETIME)''')

# define constant variables
months = {}
for m in month_name[1:]:
    if len(m) > 5:
        months[m] = [m.lower(), m[:3].lower()]
    else:
        months[m] = [m.lower()]
WORDS_TO_EXCLUDE = ['super']


def send_mail(email, slot_date):
    message = emails.html(
    html=f"<h1>SLOT UPDATE!</h1><h3><br> Slot is available on {slot_date.strftime('%d %B')}</h3>",
    subject=f"Slot available on {slot_date.strftime('%d %B')}",
    mail_from=("US F1 SLOT BOT", "noreply_slot_bot@zubayer.one"))

    message.send(
        to=email,
        smtp={"host": "email-smtp.us-east-1.amazonaws.com",
            "port": 587,
            "user": SMTP_USER,
            "password": SMTP_PASS,
            "tls": True}
    )
    print("Sent mail to:", email)


def save_and_notify(slot_date, updated):
    """
    Save the slot date to file and check for alarms in database
    """

    # save the date in database
    cursor.execute('''INSERT OR REPLACE INTO data (id, slot_date, updated) VALUES (?, ?, ?)''', (1, slot_date, updated))
    conn.commit()

    cursor.execute(
        '''SELECT * FROM alarms WHERE notif_date >= ?''', (slot_date,))
    
    results = cursor.fetchall()
    for row in results:
        print(row)
        send_mail(row[1], slot_date)


def check_closeness(dates: list, month_names: list, s: str) -> int:
    """
    Check if the date is close to the month name
    """
    for date in dates:
        date_ind = s.find(date)
        if any(m in s[max(0, date_ind-15):date_ind+15] for m in month_names):
            return int(date)
    return 0


def get_date(msg):
    """
    Get slot date from message
    """
    text = msg.text.lower()
    updated = msg.date.astimezone(pytz.timezone('Asia/Dhaka'))
    current_year = dt.datetime.now().year

    if not (any(word in text for word in WORDS_TO_EXCLUDE) or text.endswith('?')):    
        for big_name, m in months.items():
            if any(each in text for each in m):
                dates = re.findall(r"\d{1,2}", text)
                if dates:
                    # check if the date is close to the monthname in string
                    result_date = check_closeness(dates, m, text)
                    if result_date:
                        slot_datetime = dt.datetime.strptime(
                            f"{current_year} {result_date} {big_name}", "%Y %d %B")
                        save_and_notify(slot_datetime.date(), updated)
                        return {
                            "slot_date": slot_datetime.date(),
                            "updated": updated
                        }
    return False


# initialize telegram client
client = TelegramClient("slot_checker", api_id, api_hash)
client.start()

# listen for new messages


@client.on(events.NewMessage(-1001403807365))
async def handle_new_message(event):
    """
    Handler for new messages
    """
    print(event.message.text, event.message.date)
    result = get_date(event.message)
    if result:
        print(f"Available slot date: {result['slot_date'].strftime('%d %B')}")
        print(f"Last updated at: {result['updated']}")
    print("\n\n")

client.run_until_disconnected()
