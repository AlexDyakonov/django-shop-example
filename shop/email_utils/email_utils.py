from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings


def send_registration_email(user):
    html_message = render_to_string('email/registration_email.html', {'user': user})
    subject = 'Поздравляем с успешной регистрацией'
    message = 'Добро пожаловать! Ваша почта для входа в аккаунт:' + str(user.email)
    send_mail(subject, message, settings.EMAIL_HOST_USER , [user.email], html_message=html_message)         

def send_order_confirmation_email(user, order_id, amount, order_date):
    html_message = render_to_string('email/order_confirmation.html', {
        'user': user,
        'order_id': order_id,
        'amount': amount,
        'order_date': order_date,
    })
    subject = 'Успешное создание и оплата заказа'
    message = 'Спасибо за ваш заказ'
    send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email], html_message=html_message)

def send_create_order_mail(user, order_id, order_amount, payment_link):
    html_message = render_to_string('email/create_order.html', {
        'user': user,
        'order_id': order_id,
        'order_amount': order_amount,
        'payment_link': payment_link,
    })

    subject = 'Заказ #{} успешно создан: ожидается оплата'.format(order_id)
    message = 'Спасибо за ваш заказ. Пожалуйста, выполните оплату по ссылке: {}'.format(payment_link)

    send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email], html_message=html_message)

def send_cancel_order_mail(user, order_id):
    html_message = render_to_string('email/cancel_order.html', {
        'user': user,
        'order_id': order_id,
    })

    subject = 'Отмена оплаты заказа #{}'.format(order_id)
    message = 'Сожалеем, оплата для вашего заказа была отменена.'

    send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email], html_message=html_message)

def send_password_change_mail(user):
    html_message = render_to_string('email/password_change.html', {
        'user': user,
    })

    subject = 'Успешная смена пароля'
    message = 'Ваш пароль был успешно изменен для аккаунта.'

    send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email], html_message=html_message)