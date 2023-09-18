import json
from coinbase_commerce.webhook import Webhook
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views import View

class CoinbaseWebhook(View):
    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        payload = json.loads(request.body.decode('utf-8'))
        webhook_secret = 'test'  
        try:
            event = Webhook.construct_event(
                payload,
                request.headers.get('X-CC-Webhook-Signature'),
                webhook_secret
            )
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

        if event['type'] == 'charge:confirmed':

            return JsonResponse({'status': 'success'})

        return JsonResponse({'status': 'success'})
