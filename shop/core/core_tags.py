from django import template
from core.models import *

# TODO Оптимизировать | заменить все что возможно на теги

register = template.Library()

@register.simple_tag(name='getcats')
def get_categories():
    return Category.objects.all()