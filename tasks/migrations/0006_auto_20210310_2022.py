# Generated by Django 3.0.6 on 2021-03-11 02:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0005_auto_20210120_1150'),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name='task',
            name='tasks_task_task_ty_45f0a7_idx',
        ),
        migrations.RemoveField(
            model_name='task',
            name='task_type',
        ),
    ]
