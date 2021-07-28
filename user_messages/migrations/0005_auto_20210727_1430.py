# Generated by Django 3.2.3 on 2021-07-27 14:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tasks', '0014_auto_20210720_1801'),
        ('user_messages', '0004_auto_20210726_2321'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usermessagethread',
            name='participant',
        ),
        migrations.AddField(
            model_name='usermessagethread',
            name='created_by',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='message_thread_created_by', to='users.customuser'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='usermessagethread',
            name='recipient',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='message_thread_recipients', to='users.customuser'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='usermessagethread',
            name='job',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='message_thread_jobs', to='tasks.task'),
        ),
    ]
