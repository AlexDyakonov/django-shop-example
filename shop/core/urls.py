from django.urls import path, re_path
from core.views import *

app_name = "core"

urlpatterns = [
    path('', index, name='home'),
    path('about/', about),
    path('items/', showcase),
    path('item/number/', item)
]
