# Generated by Django 3.1.5 on 2021-01-11 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_product_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, default='placeholder.jpg', null=True, upload_to=''),
        ),
    ]