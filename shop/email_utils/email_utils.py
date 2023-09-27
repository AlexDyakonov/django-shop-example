from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.translation import gettext as _

def send_registration_email(user):
    html_message = render_to_string('email/registration_email.html', {'user': user})
    subject = _('Поздравляем с успешной регистрацией')
    message = _('Добро пожаловать! Ваша почта для входа в аккаунт:') + str(user.email)
    send_mail(subject, message, settings.EMAIL_HOST_USER , [user.email], html_message=html_message)         

def send_order_confirmation_email(user, order_id, amount, order_date):
    html_message = render_to_string('email/order_confirmation.html', {
        'user': user,
        'order_id': order_id,
        'amount': amount,
        'order_date': order_date,
    })
    subject = _('Успешное создание и оплата заказа')
    message = _('Спасибо за ваш заказ')
    send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email], html_message=html_message)

def send_create_order_mail(user, order_id, order_amount, payment_link):
    html_message = render_to_string('email/create_order.html', {
        'user': user,
        'order_id': order_id,
        'order_amount': order_amount,
        'payment_link': payment_link,
    })

    subject = _('Заказ #{} успешно создан: ожидается оплата'.format(order_id))
    message = _('Спасибо за ваш заказ. Пожалуйста, выполните оплату по ссылке: {}').format(payment_link)

    send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email], html_message=html_message)

def send_cancel_order_mail(user, order_id):
    html_message = render_to_string('email/cancel_order.html', {
        'user': user,
        'order_id': order_id,
    })

    subject = _('Отмена оплаты заказа #{}').format(order_id)
    message = _('Сожалеем, оплата для вашего заказа была отменена.')

    send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email], html_message=html_message)

def send_password_change_mail(user):
    html_message = render_to_string('email/password_change.html', {
        'user': user,
    })

    subject = _('Успешная смена пароля')
    message = _('Ваш пароль был успешно изменен для аккаунта.')

    send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email], html_message=html_message)