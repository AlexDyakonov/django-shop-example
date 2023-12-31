# Generated by Django 4.2.4 on 2023-09-20 05:44

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_alter_product_product_status_payment'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='total',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='product',
            name='product_status',
            field=models.CharField(choices=[('draft', 'Draft'), ('published', 'Published'), ('disabled', 'Disabled')], default='draft', max_length=10),
        ),
    ]
