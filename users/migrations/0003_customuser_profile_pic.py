# Generated by Django 3.0.6 on 2020-06-15 01:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20200526_1349'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='profile_pic',
            field=models.ImageField(default='', upload_to='images/'),
            preserve_default=False,
        ),
    ]
