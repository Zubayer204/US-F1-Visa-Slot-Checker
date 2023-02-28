from os import getenv
from dotenv import load_dotenv
from telethon import TelegramClient, events


# get app credentials
load_dotenv()
api_id = int(getenv('API_ID'))
api_hash = getenv('API_HASH')

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

client.run_until_disconnected()
