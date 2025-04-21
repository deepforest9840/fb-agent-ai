from email.message import EmailMessage
import smtplib
import ssl

emailSender = 'bidcraft27@gmail.com'
emailPassword = 'bchn ltho thde gvqd'

def sendEmail(subject: str, body: str, receiver_email: str):
    message = EmailMessage()
    message.set_content(body)
    message["Subject"] = subject
    message["From"] = emailSender
    message["To"] = receiver_email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(emailSender, emailPassword)
        server.send_message(message)