# Generated by Django 4.2.4 on 2023-09-28 19:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0043_category_slug_product_slug_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(max_length=255, unique=True, verbose_name='URL'),
        ),
        migrations.AlterField(
            model_name='product',
            name='slug',
            field=models.SlugField(max_length=255, unique=True, verbose_name='URL'),
        ),
    ]
