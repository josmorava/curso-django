# Generated by Django 5.0.6 on 2024-08-13 21:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_alter_product_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='images/', verbose_name='Foto'),
        ),
    ]
