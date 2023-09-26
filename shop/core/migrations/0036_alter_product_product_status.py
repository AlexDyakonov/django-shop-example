# Generated by Django 4.2.4 on 2023-09-26 17:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0035_category_title_en_category_title_ru_country_title_en_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product_status',
            field=models.CharField(choices=[('draft', 'Draft'), ('published', 'Published'), ('disabled', 'Disabled')], default='draft', max_length=10),
        ),
    ]
