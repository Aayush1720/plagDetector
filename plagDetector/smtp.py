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
message['From'] = '⛳ Capture-The-Plag ⛳'
message['To'] = 'aadarsh.goyal11@gmail.com;aayushchoubey19@cse.iiitp.ac.in;tanmaymodi19@cse.iiitp.ac.in;prasaddalwee19@cse.iiitp.ac.in'
# message['CC'] = 'contact@company.com'
message['Subject'] = 'Plagiarism Report - CTP'

# message for the user to be updated
assignment_name = "ass3"
msg_content = f'Hi There,<br><br> Please find the attached auto generated report for your plagiarism-check of the assignment - {assignment_name}.<br><br>Regards, <br>Capture-The-Plag'
body = MIMEText(msg_content, 'html')
message.attach(body)

attachmentPath = f"../reports/{assignment_name}.docx"
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
