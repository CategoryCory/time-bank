# Generated by Django 3.0.6 on 2021-01-25 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_customuser_sullivan_coins_balance'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='skills',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
