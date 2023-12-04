import pandas as pd
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib, ssl
from model.SubUser import SubUser
from app import app

# email_password = app.config['EMAIL_PASSWORD']
email_password = 'qcbx wfzf eysm xlxk'

# sends an email
def send_email(df:pd.DataFrame, email:str):
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = 'hdbresalealertservice@gmail.com'
    receiver_email  = email
    password = email_password
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

def send_email_template(email:str, header:str, footer:str, with_df:bool == None, df:pd.DataFrame == None):
    try:
        port = 465  # For SSL
        smtp_server = "smtp.gmail.com"
        service_email = 'hdbresalealertservice@gmail.com'
        password = email_password
        message = MIMEMultipart()
        if (with_df):
            html_table = df.to_html(index=False)
            # Attach HTML content to the email
            html_body = f'<html><body>{header} <br> {html_table} <br> {footer} </body></html>'
            message.attach(MIMEText(html_body, 'html'))
        else:
            html_body = f'<html><body><div>{header}<br>{footer}</div></body></html>'
            message.attach(MIMEText(html_body, 'html'))
        message['From'] = service_email
        message['To'] = email
        message['Subject'] = "HDB Resale Alert"
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
def send_confirmation_email(new_user:SubUser, confirmation_link:str):
    try:
        print("Entering send confirmation email")
        port = 465  # For SSL
        smtp_server = "smtp.gmail.com"
        sender_email = 'hdbresalealertservice@gmail.com'
        receiver_email  = new_user.email
        password = email_password
        domainname = "localhost:5000"
        message = MIMEMultipart()
        body = f"""
<p>You are signing up for HDB Resale Price Alerts with the following search parameters:</p>
<ul>
    <li>Street name: {new_user.streetName}</li>
    <li>Flat Type: {new_user.flatType}</li>
    <li>Blk From: {new_user.blkFrom}</li>
    <li>Blk To: {new_user.blkTo}</li>
</ul>
<br>
<p>Please click the following link to confirm your email: <a href="http://{domainname + confirmation_link}" style="color: #3498db; text-decoration: underline;">Confirm Email</a></p>

        """
        html_body = f'<html><body>{body}</body></html>'
        message.attach(MIMEText(html_body, 'html'))
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
    except Exception as ex:
        print(f"Unable to send email due to {ex} ")  
