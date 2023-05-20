from api_yamdb.settings import ADMIN_EMAIL
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail


def send_email(user):
    confirmation_code = default_token_generator.make_token(user)
    email_subject = 'Код для авторизации'
    email_text = f'Ваш код для авторизации - {confirmation_code}'
    admin_email = ADMIN_EMAIL
    user_email = [user.email]
    return send_mail(email_subject, email_text, admin_email, user_email)
