# Generated by Django 3.0.6 on 2020-06-18 01:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tasks', '0002_auto_20200617_1947'),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150)),
                ('description', models.TextField()),
                ('expires_on', models.DateField(default=django.utils.timezone.now, null=True)),
                ('task_type', models.CharField(choices=[('REQUEST', 'Request'), ('OFFER', 'Offer')], max_length=20)),
                ('frequency', models.CharField(choices=[('ONE_TIME', 'One Time'), ('DAILY', 'Daily'), ('WEEKLY', 'Weekly'), ('BIWEEKLY', 'Biweekly'), ('MONTHLY', 'Monthly'), ('AS_NEEDED', 'As Needed')], max_length=20)),
                ('status', models.CharField(choices=[('AVAILABLE', 'Available'), ('UNAVAILABLE', 'Unavailable'), ('COMPLETED', 'Completed'), ('DELETED', 'Deleted')], default='AVAILABLE', max_length=20)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddIndex(
            model_name='task',
            index=models.Index(fields=['title'], name='tasks_task_title_6b13c2_idx'),
        ),
        migrations.AddIndex(
            model_name='task',
            index=models.Index(fields=['task_type'], name='tasks_task_task_ty_45f0a7_idx'),
        ),
        migrations.AddIndex(
            model_name='task',
            index=models.Index(fields=['status'], name='tasks_task_status_4a0a95_idx'),
        ),
    ]
