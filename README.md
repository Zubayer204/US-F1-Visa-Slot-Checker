# US F1 Slot Bot
The code is divided into two sections. One receives the text message from telegram group, parses it and stores it on local SQLite database. Another one is the flask web server. That's where people can see the available date as well as set/delete alerts using their email.

## Prerequisites
1. We will need a few things first. Since we are reading text messages from the telegram group, we will need telegram API keys. We will be using **Telegram API**, not the **Bot API**. Go to https://my.telegram.org/auth?to=apps and create an app. Get the API_ID and API_HASH from there and save it in the .env file. 
2. We will be sending email to alert. So prepare your SMTP credentials and store that in .env file as well.

## message_receiver.py
This is the heart of our program. This python program will read for incoming text messages in the telegram group, parse the date from text and send emails to the appropriate people. We will have to run this python file 24/7 to get the updates 24/7. We can do so in a simple way using [`screen`](https://www.howtogeek.com/662422/how-to-use-linuxs-screen-command/) in linux.

## Flask Server
Our ```app.py``` is the flask server. This is the website that we will host to see the latest date as well as set/delete alerts using email. We will need to host this server from the same folder where `message_receiver.py` file is running. Hosting flask servers is a broad term and I suggest reading [this article](https://docs.digitalocean.com/tutorials/app-deploy-flask-app/) from digitalocean.

## License

MIT

**Free Software, Hell Yeah!**
