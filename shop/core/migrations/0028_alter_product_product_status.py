# Generated by Django 4.2.4 on 2023-09-24 22:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0027_remove_payment_charge_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product_status',
            field=models.CharField(choices=[('disabled', 'Disabled'), ('draft', 'Draft'), ('published', 'Published')], default='draft', max_length=10),
        ),
    ]
