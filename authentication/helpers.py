from django.core.mail import send_mail
from django.conf import settings


def send_forget_password_email(email, token):
    subject = 'Your Forget Password Token'
    message = f'Hi, Your code to reset your password copy it and paste it in the app\n{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject=subject, message=message, from_email=email_from, recipient_list=recipient_list)
    return True


def send_email_verification_email(email, token):
    subject = 'Your email verification Token'
    message = f'Hi, Your code to verify your email copy it and paste it in the app\n{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject=subject, message=message, from_email=email_from, recipient_list=recipient_list)
    return True