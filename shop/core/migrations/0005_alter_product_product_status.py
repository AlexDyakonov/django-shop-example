# Generated by Django 4.2.4 on 2023-09-08 21:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_alter_product_product_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product_status',
            field=models.CharField(choices=[('rejected', 'rejected'), ('in_review', 'In review'), ('published', 'Published'), ('disabled', 'Disabled'), ('draft', 'Draft')], default='in_review', max_length=10),
        ),
    ]
