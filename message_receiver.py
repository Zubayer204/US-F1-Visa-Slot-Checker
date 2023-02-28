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
months = {m.lower() for m in month_name[1:]}


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


def get_date(msg):
    """
    Get slot date from message
    """
    text = msg.text.lower()
    updated = msg.date.astimezone(pytz.timezone('Asia/Dhaka'))
    current_year = dt.datetime.now().year

    for m in months:
        if m in text or m[:3] in text:
            date = re.search(r"\d{1,2}", text)
            if date:
                slot_datetime = dt.datetime.strptime(
                    f"{current_year} {date.group()} {m.capitalize()}", "%Y %d %B")
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
