# Generated by Django 3.0.6 on 2021-03-11 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userreview',
            name='comments',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
