from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import smtplib
from django.conf import settings


from django.core.mail import EmailMessage


def send_email(recipient_email, pdf_file_path):

    email_host_user = settings.EMAIL_HOST_USER
    email_pass_host_user = settings.EMAIL_HOST_PASSWORD
    EMAIL_PORT = settings.EMAIL_PORT


    subject = 'OLIVY wanted to inform you!'
    file_path='disease_reports/Aculos_rapport.pdf'

    with open(file_path, 'rb') as f:
        file_data = f.read()
        file_name = f.name

    email = EmailMessage(
        subject,
        'tthis is the Body!',
        email_host_user,
        ['ellabouhawel@gmail.com'],
    )

    email.attach(file_name, file_data, 'application/pdf')
    email.send()
    print ('email sent successfully !')



    import smtplib

def send_email(subject, body, to, gmail_user, gmail_password):
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_password)
        message = f'Subject: {subject}\n\n{body}'
        server.sendmail(gmail_user, to, message)
        server.quit()
        print('Email sent successfully')
    except Exception as e:
        print(f'Something went wrong... {e}')

# usage
send_email('Test Subject', 'This is a test email', 'ellabouhawel@gmail.com',  'info.Olivy@gmail.com', 'j/UrEZK0AfKmvU6fY9xpYDr9fC5wlK5dBLJQ/9+1dvc=')
