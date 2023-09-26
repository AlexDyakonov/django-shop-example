from modeltranslation.translator import register, TranslationOptions
from core.models import Category, Product, Country


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('title',)

@register(Country)
class CountryTranslationOptions(TranslationOptions):
    fields = ('title',)

@register(Product)
class ProductTranslationOptions(TranslationOptions):
    fields = ('title', 'description',)