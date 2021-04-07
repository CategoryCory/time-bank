# Generated by Django 3.0.6 on 2021-04-07 03:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0010_auto_20210406_2019'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taskcategory',
            name='parent_category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subcategory', to='tasks.TaskCategory'),
        ),
    ]