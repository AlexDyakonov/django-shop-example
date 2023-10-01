# Generated by Django 4.2.4 on 2023-09-27 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0040_alter_product_product_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product_status',
            field=models.CharField(choices=[('published', 'Published'), ('disabled', 'Disabled'), ('draft', 'Draft')], default='draft', max_length=10),
        ),
    ]