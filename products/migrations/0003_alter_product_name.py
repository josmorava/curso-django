# Generated by Django 5.0.6 on 2024-07-02 21:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_alter_product_available_alter_product_description_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.TextField(max_length=100, verbose_name='Nombre'),
        ),
    ]
