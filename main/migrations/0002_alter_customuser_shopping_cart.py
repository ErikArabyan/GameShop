# Generated by Django 5.1.1 on 2024-09-18 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='shopping_cart',
            field=models.ManyToManyField(related_name='cart', to='main.game'),
        ),
    ]
