# Generated by Django 3.1.5 on 2021-01-18 20:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_auto_20210111_1728'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='transaction',
            new_name='transaction_id',
        ),
    ]
