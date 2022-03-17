import json
from smtplib import SMTP
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import markdown


DISPLAY_NAME = ""
SENDER_EMAIL = ""
PASSWORD = ""

def send_emails(server: SMTP, message: str, tolist: dict):
    sent_count = 0
    
    for nickname, receiver in tolist.items():

        multipart_msg = MIMEMultipart("alternative")

        multipart_msg["Subject"] = DISPLAY_NAME
        multipart_msg["From"] = nickname + f' <{SENDER_EMAIL}>'
        multipart_msg["To"] = receiver

        text = message
        html = markdown.markdown(text)

        part1 = MIMEText(text, "plain")
        part2 = MIMEText(html, "html")

        multipart_msg.attach(part1)
        multipart_msg.attach(part2)

        try:
            server.sendmail(SENDER_EMAIL, receiver,
                            multipart_msg.as_string())
        except Exception as err:
            print(f'Problem occurend while sending to {receiver} ')
            print(err)
            input("PRESS ENTER TO CONTINUE")
        else:
            sent_count += 1

    print(f"Sent {sent_count} emails")


def start_email(message: str):
    global DISPLAY_NAME
    global SENDER_EMAIL
    global PASSWORD
    # load json datas
    with open('config.json', encoding='utf-8') as f:
        json_datas = json.load(f)
    DISPLAY_NAME = json_datas['EmailInfo']['displayName']
    SENDER_EMAIL = json_datas['EmailInfo']['senderEmail']
    PASSWORD = json_datas['EmailInfo']['password']

    host = "smtp.qq.com"
    port = 587  # TLS replaced SSL in 1999
    server = SMTP(host=host, port=port)
    server.connect(host=host, port=port)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(user=SENDER_EMAIL, password=PASSWORD)
    
    send_emails(server, message, json_datas['ToList'])
        
    server.quit()