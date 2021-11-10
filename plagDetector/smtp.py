import smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import secrets

smtp_server = 'smtp.gmail.com'
smtp_port = 587
# Replace with your own gmail account
gmail = secrets.EMAIL
password = secrets.PASSWORD

message = MIMEMultipart('mixed')
message['From'] = 'Contact <{sender}>'.format(sender=gmail)
message['To'] = 'aadarsh.goyal11@gmail.com;aayushchoubey19@cse.iiitp.ac.in;tanmaymodi19@cse.iiitp.ac.in;prasaddalwee19@cse.iiitp.ac.in'
# message['CC'] = 'contact@company.com'
message['Subject'] = 'Hello from smtp'

# message for the user to be updated
msg_content = '<h4>Hi There,<br> This is a testing message.</h4>\n'
body = MIMEText(msg_content, 'html')
message.attach(body)

attachmentPath = "../media/B_Tech - 5th CSE- New TT.pdf"
try:
    with open(attachmentPath, "rb") as attachment:
        p = MIMEApplication(attachment.read(), _subtype="pdf")
        p.add_header('Content-Disposition', "attachment; filename= %s" % attachmentPath.split("/")[-1])
        message.attach(p)
except Exception as e:
    print(str(e))

msg_full = message.as_string()
context = ssl.create_default_context()

to = message['To']
cc = message['CC']

with smtplib.SMTP(smtp_server, smtp_port) as server:
    server.ehlo()
    server.starttls(context=context)
    server.ehlo()
    server.login(gmail, password)
    server.sendmail(gmail, to.split(";") + (cc.split(";") if cc else []), msg_full)
    server.quit()

print("email sent out successfully")
