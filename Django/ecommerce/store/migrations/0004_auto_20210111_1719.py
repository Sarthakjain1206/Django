# Generated by Django 3.1.5 on 2021-01-11 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_auto_20210111_1716'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, default='images/placeholder.jpg', null=True, upload_to=''),
        ),
    ]
