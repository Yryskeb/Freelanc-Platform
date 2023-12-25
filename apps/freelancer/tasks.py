from django.conf import settings
from twilio.rest import Client 
from django.core.mail import send_mail 
from django.utils.html import format_html
from celery import shared_task
import uuid

@shared_task()
def send_confirmation_email(email, code):
    activation_url = f'http://13.50.5.59/api/v1/freelancer/activate/?u={code}'
    html_message = format_html('''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Активация аккаунта</title>
        </head>
        <body>
            <p>Здравствуйте!</p>
            <p>Для активации вашего аккаунта перейдите по следующей ссылке:</p>
            <a href="{}">{}</a>
            <p>Спасибо!</p>
        </body>
        </html>
    ''', activation_url, activation_url)

    send_mail(
        'Активируйте ваш аккаунт!',
        '',
        'killer@gmail.com',
        [email],
        fail_silently=False,
        html_message=html_message,
    )


def send_activation_sms(phone_number, activation_code):
    message = f'Ваш код активации: {activation_code}'
    client = Client(settings.TWILIO_SID, settings.TWILIO_AUTH_TOKEN)
    client.messages.create(body=message, from_=settings.TWILIO_SENDER_PHONE, to=phone_number)



@shared_task()
def reset_password(email):
    namespace = uuid.UUID('6ba7b810-9dad-11d1-80b4-00c04fd430c8')
    sure = uuid.uuid3(namespace, email)
    reset_link = f'http://13.50.5.59/api/v1/freelancer/reset/new/password/?make_sure={sure}'

    html_message = format_html('''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Вастанавить пароль</title>
        </head>
        <body>
            <p>Здравствуйте!</p>
            <p>Для вастанавление вашего пароля перейдите по следующей ссылке:</p>
            <a href="{}">{}</a>
            <p>Спасибо!</p>
        </body>
        </html>
    ''', reset_link, reset_link)

    send_mail(
        'Password Reset',
        '',
        'some@mail.com',
        [email],
        fail_silently=False,
        html_message=html_message,
    )