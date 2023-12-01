import pandas as pd
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib, ssl



# sends an email
def send_email(df:pd.DataFrame, email:str):
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = 'hdbresalealertservice@gmail.com'
    receiver_email  = email
    password = "qcbx wfzf eysm xlxk"
    html_table = df.to_html(index=False)
    # Attach HTML content to the email
    message = MIMEMultipart()
    html_body = f'<html><body>{html_table}</body></html>'
    message.attach(MIMEText(html_body, 'html'))
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = "HDB Resale Alert"
    try:
        print(f"attempting to send email with following params -> from: {message['From']} To: {message['To']} Subject: {message['Subject']}")
        print(f"With email body : {html_body}")
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
        print("Email sent!")
    except Exception as ex:
        print(f"Unable to send email due to {ex} ")

def send_email_template(email:str, content:str, with_df:bool == None, df:pd.DataFrame == None):
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    service_email = 'hdbresalealertservice@gmail.com'
    password = "qcbx wfzf eysm xlxk"
    message = MIMEMultipart()
    if (with_df):
        html_table = df.to_html(index=False)
        # Attach HTML content to the email
        html_body = f'<html><body>{html_table}</body></html>'
        message.attach(MIMEText(html_body, 'html'))
    else:
        html_body = f'<html><body><div>{content}</div></body></html>'
        message.attach(MIMEText(html_body, 'html'))
    message['From'] = service_email
    message['To'] = email
    message['Subject'] = "HDB Resale Alert"
    try:
        print(f"attempting to send email with following params -> from: {message['From']} To: {message['To']} Subject: {message['Subject']}")
        print(f"With email body : {html_body}")
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(service_email, password)
            server.sendmail(service_email, email, message.as_string())
        print("Email sent!")
    except Exception as ex:
        print(f"Unable to send email due to {ex} ")

# def send_confirmation_email(email:str, confirmation_link:str):
#     content = f'You are signing up for HDB Resale Price Alerts. Please click the following link to confirm your email: {confirmation_link}'
#     send_email_template(email,content)

# sends an email
def send_confirmation_email(email:str, confirmation_link:str):
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = 'hdbresalealertservice@gmail.com'
    receiver_email  = email
    password = "qcbx wfzf eysm xlxk"
    body = f'You are signing up for HDB Resale Price Alerts. Please click the following link to confirm your email: {confirmation_link}'
    message = MIMEText(body)
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = "HDB Resale Alert"
    try:
        print(f"attempting to send email with following params -> from: {message['From']} To: {message['To']} Subject: {message['Subject']}")
        print(f"With email body : {message}")
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
        print("Email sent!")
    except Exception as ex:
        print(f"Unable to send email due to {ex} ")