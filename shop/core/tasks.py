from celery import shared_task
from django.utils import timezone
from .models import Payment

@shared_task
def delete_payment(charge_id):
    try:
        payment = Payment.objects.get(charge_id=charge_id)
        if timezone.now() - payment[0].created_at > timezone.timedelta(hours=1):
            payment.delete()
    except Payment.DoesNotExist:
        pass