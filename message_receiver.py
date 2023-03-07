from os import getenv
from calendar import month_name
from multiprocessing import Process
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
WORDS_TO_EXCLUDE = ['super', 'nah', 'nai', 'not', 'grateful', 'thanks', 'gone']


def send_mail(email, slot_date):
    """
    Function for sending mails to the subscribers
    """
    message = emails.html(
        html=f"""<!DOCTYPE html>
<html xmlns:v="urn:schemas-microsoft-com:vml" xmlns:o="urn:schemas-microsoft-com:office:office" lang="en">

<head>
	<title></title>
	<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
	<!--[if mso]><xml><o:OfficeDocumentSettings><o:PixelsPerInch>96</o:PixelsPerInch><o:AllowPNG/></o:OfficeDocumentSettings></xml><![endif]-->
	<style>
		* {{
			box-sizing: border-box;
		}}

		body {{
			margin: 0;
			padding: 0;
		}}

		a[x-apple-data-detectors] {{
			color: inherit !important;
			text-decoration: inherit !important;
		}}

		#MessageViewBody a {{
			color: inherit;
			text-decoration: none;
		}}

		p {{
			line-height: inherit
		}}

		.desktop_hide,
		.desktop_hide table {{
			mso-hide: all;
			display: none;
			max-height: 0px;
			overflow: hidden;
		}}

		.image_block img+div {{
			display: none;
		}}

		@media (max-width:720px) {{
			.social_block.desktop_hide .social-table {{
				display: inline-block !important;
			}}

			.image_block img.big,
			.row-content {{
				width: 100% !important;
			}}

			.mobile_hide {{
				display: none;
			}}

			.stack .column {{
				width: 100%;
				display: block;
			}}

			.mobile_hide {{
				min-height: 0;
				max-height: 0;
				max-width: 0;
				overflow: hidden;
				font-size: 0px;
			}}

			.desktop_hide,
			.desktop_hide table {{
				display: table !important;
				max-height: none !important;
			}}
		}}
	</style>
</head>

<body style="background-color: #ffffff; margin: 0; padding: 0; -webkit-text-size-adjust: none; text-size-adjust: none;">
	<table class="nl-container" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; background-color: #ffffff;">
		<tbody>
			<tr>
				<td>
					<table class="row row-1" align="center" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; background-color: #7787b5;">
						<tbody>
							<tr>
								<td>
									<table class="row-content stack" align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; color: #000000; width: 700px;" width="700">
										<tbody>
											<tr>
												<td class="column column-1" width="100%" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; font-weight: 400; text-align: left; vertical-align: top; border-top: 0px; border-right: 0px; border-bottom: 0px; border-left: 0px;">
													<div class="spacer_block" style="height:10px;line-height:10px;font-size:1px;">&#8202;</div>
												</td>
											</tr>
										</tbody>
									</table>
								</td>
							</tr>
						</tbody>
					</table>
					<table class="row row-2" align="center" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; background-color: #e9e9f6; background-image: url('https://d1oco4z2z1fhwp.cloudfront.net/templates/default/1016/Patternvirus.png'); background-position: center top; background-repeat: repeat;">
						<tbody>
							<tr>
								<td>
									<table class="row-content stack" align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; color: #000000; width: 700px;" width="700">
										<tbody>
											<tr>
												<td class="column column-1" width="100%" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; font-weight: 400; text-align: left; padding-bottom: 45px; padding-left: 15px; padding-right: 15px; padding-top: 35px; vertical-align: top; border-top: 0px; border-right: 0px; border-bottom: 0px; border-left: 0px;">
													<table class="text_block block-1" width="100%" border="0" cellpadding="10" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; word-break: break-word;">
														<tr>
															<td class="pad">
																<div style="font-family: sans-serif">
																	<div class style="font-size: 12px; font-family: Roboto, Tahoma, Verdana, Segoe, sans-serif; mso-line-height-alt: 14.399999999999999px; color: #50639c; line-height: 1.2;">
																		<p style="margin: 0; font-size: 12px; text-align: center; mso-line-height-alt: 14.399999999999999px;"><strong><span style="font-size:38px;">SLOT UPDATE!</span></strong></p>
																	</div>
																</div>
															</td>
														</tr>
													</table>
													<table class="image_block block-2" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;">
														<tr>
															<td class="pad" style="width:100%;padding-right:0px;padding-left:0px;">
																<div class="alignment" align="center" style="line-height:10px"><a href="https://slotbot.zubayer.one/" target="_blank" style="outline:none" tabindex="-1"><img class="big" src="https://live.staticflickr.com/65535/48937388902_8c37fac212_b.jpg" style="display: block; height: auto; border: 0; width: 670px; max-width: 100%;" width="670" alt="Image" title="Image"></a></div>
															</td>
														</tr>
													</table>
												</td>
											</tr>
										</tbody>
									</table>
								</td>
							</tr>
						</tbody>
					</table>
					<table class="row row-3" align="center" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;">
						<tbody>
							<tr>
								<td>
									<table class="row-content stack" align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; color: #000000; width: 700px;" width="700">
										<tbody>
											<tr>
												<td class="column column-1" width="100%" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; font-weight: 400; text-align: left; padding-bottom: 55px; padding-top: 30px; vertical-align: top; border-top: 0px; border-right: 0px; border-bottom: 0px; border-left: 0px;">
													<table class="heading_block block-1" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;">
														<tr>
															<td class="pad" style="text-align:center;width:100%;">
																<h1 style="margin: 0; color: #555555; direction: ltr; font-family: Roboto, Tahoma, Verdana, Segoe, sans-serif; font-size: 28px; font-weight: 700; letter-spacing: normal; line-height: 120%; text-align: center; margin-top: 0; margin-bottom: 0;"><em><span class="tinyMce-placeholder">SLOT IS AVAILABLE ON {slot_date.strftime('%d %B')}!</span></em></h1>
															</td>
														</tr>
													</table>
												</td>
											</tr>
										</tbody>
									</table>
								</td>
							</tr>
						</tbody>
					</table>
					<table class="row row-4" align="center" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; background-color: #f7f7ff;">
						<tbody>
							<tr>
								<td>
									<table class="row-content stack" align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; color: #000000; width: 700px;" width="700">
										<tbody>
											<tr>
												<td class="column column-1" width="100%" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; font-weight: 400; text-align: left; padding-bottom: 5px; padding-left: 10px; padding-right: 10px; padding-top: 25px; vertical-align: top; border-top: 0px; border-right: 0px; border-bottom: 0px; border-left: 0px;">
													<table class="social_block mobile_hide block-1" width="100%" border="0" cellpadding="10" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;">
														<tr>
															<td class="pad">
																<div class="alignment" align="center">
																	<table class="social-table" width="138.66666666666666px" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; display: inline-block;">
																		<tr>
																			<td style="padding:0 7px 0 7px;"><a href="https://instagram.com/zubayer204" target="_blank"><img src="https://app-rsrc.getbee.io/public/resources/social-networks-icon-sets/circle-blue/instagram@2x.png" width="32" height="32" alt="Instagram" title="Instagram" style="display: block; height: auto; border: 0;"></a></td>
																			<td style="padding:0 7px 0 7px;"><a href="https://github.com/Zubayer204" target="_blank"><img src="https://ff5e0e4847.imgdist.com/public/users/BeeFree/beefree-964jj0dqkah/github-mark.svg" width="32.666666666666664" height="32" alt="Github" title="Github" style="display: block; height: auto; border: 0;"></a></td>
																			<td style="padding:0 7px 0 7px;"><a href="https://www.linkedin.com/in/zuba-the-coder/" target="_blank"><img src="https://app-rsrc.getbee.io/public/resources/social-networks-icon-sets/circle-blue/linkedin@2x.png" width="32" height="32" alt="LinkedIn" title="LinkedIn" style="display: block; height: auto; border: 0;"></a></td>
																		</tr>
																	</table>
																</div>
															</td>
														</tr>
													</table>
													<div class="spacer_block" style="height:30px;line-height:30px;font-size:1px;">&#8202;</div>
												</td>
											</tr>
										</tbody>
									</table>
								</td>
							</tr>
						</tbody>
					</table>
				</td>
			</tr>
		</tbody>
	</table><!-- End -->
</body>

</html>""",
        subject=f"Slot available on {slot_date.strftime('%d %B')}",
        mail_from=("US F1 SLOT BOT", "slotbot@zubayer.one"))

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
    cursor.execute(
        '''INSERT OR REPLACE INTO data (id, slot_date, updated) VALUES (?, ?, ?)''',
        (1, slot_date, updated)
    )
    conn.commit()

    cursor.execute(
        '''SELECT * FROM alarms WHERE notif_date >= ?''', (slot_date,))

    results = cursor.fetchall()
    proccesses = []
    for row in results:
        print(row)
        process = Process(target=send_mail, args=(row[1], slot_date))
        process.start()
        proccesses.append(process)
    for process in proccesses:
        process.join()


def check_closeness(dates: list, month_names: list, text_string: str) -> int:
    """
    Check if the date is close to the month name
    """
    for date in dates:
        date_ind = text_string.find(date)
        if any(m in text_string[max(0, date_ind-10):date_ind+10] for m in month_names):
            return int(date)
    return 0


def get_date(msg):
    """
    Get slot date from message
    """
    text = msg.text.lower()
    updated = msg.date.astimezone(pytz.timezone('Asia/Dhaka'))
    current_year = dt.datetime.now().year

    if not (any(word in text.split(' ') for word in WORDS_TO_EXCLUDE) or text.endswith('?')):
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
