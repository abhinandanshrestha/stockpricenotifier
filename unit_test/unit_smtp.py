import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import unit_test.config as config

# Set up the email parameters
sender = 'shtabhi@gmail.com'
receiver = 'pubjeegamer@gmail.com'
password = config.PASSWORD
subject = 'Testing email via CLI'

# Create a message object
message = MIMEMultipart()
message['From'] = sender
message['To'] = receiver
message['Subject'] = subject

# Add the message body
body = 'This is the message body.'
message.attach(MIMEText(body, 'plain'))

# Create the SMTP server
smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
smtp_server.starttls()

# Login to the SMTP server
smtp_server.login(sender, password)

# Send the email
smtp_server.sendmail(sender, receiver, message.as_string())

# Close the SMTP server
smtp_server.quit()