# Generated by Django 3.0.6 on 2021-04-07 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0011_auto_20210406_2201'),
    ]

    operations = [
        migrations.AddField(
            model_name='taskcategory',
            name='slug',
            field=models.SlugField(default='', max_length=100),
            preserve_default=False,
        ),
    ]