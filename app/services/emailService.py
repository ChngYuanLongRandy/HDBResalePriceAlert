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