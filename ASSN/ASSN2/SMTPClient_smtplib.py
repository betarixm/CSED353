import smtplib
import logging
from email.message import EmailMessage

username = ''
password = ''            # IMPORTANT NOTE!!!!!!!!!!: PLEASE REMOVE THIS FIELD WHEN YOU SUBMIT!!!!!

msg = EmailMessage()
msg['Subject'] = 'Computer Network Assignment2 - Email Client'
msg['From'] = ''
msg['To'] = ''
msg.set_content('It is so hard for me!!!')

# 1. Connect to the mail server
client = smtplib.SMTP('smtp.office365.com', 587)
client.set_debuglevel(logging.DEBUG)

# 2. Login to the mail server
client.starttls()
client.login(username, password)
client.helo()

# 3. Send email
client.send_message(msg)

# 4. Quit to the mail server
client.quit()