# Generated by Django 3.0.6 on 2020-05-29 02:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tags', '0001_initial'),
        ('tasks', '0004_delete_tag'),
    ]

    operations = [
        migrations.AddField(
            model_name='offer',
            name='tags',
            field=models.ManyToManyField(related_name='offers', to='tags.Tag'),
        ),
        migrations.AddField(
            model_name='request',
            name='tags',
            field=models.ManyToManyField(related_name='requests', to='tags.Tag'),
        ),
    ]