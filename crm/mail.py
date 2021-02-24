import os
from sendgrid import SendGridAPIClient
from django.conf import settings
from sendgrid.helpers.mail import Mail


def sendEmail(user, template, subject):
    message = Mail(
        from_email='jpmcrain27@gmail.com',
        to_emails=user.email,
        subject=subject,
        html_content=template)
    try:
        sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
        response = sg.send(message)
        print(response.status_code)
    except Exception as e:
        print(e.message)


def sendMultipleEmails(users, subject):
    for user in users:
        message = Mail(
            from_email='jpmcrain27@gmail.com',
            to_emails=user.email,
            subject=subject,
            html_content=template)
        try:
            sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
            response = sg.send(message)
            print(response.status_code)
        except Exception as e:
            print(e.message)
