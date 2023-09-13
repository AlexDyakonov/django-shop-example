from django.urls import path, re_path
from core.views import *

app_name = "core"

urlpatterns = [
    path('', index, name='home'),
    path('help/', help, name='help'),
    path('showcase/', showcase, name='showcase'),
    path('item/<str:pid>/', show_item, name='item')
]