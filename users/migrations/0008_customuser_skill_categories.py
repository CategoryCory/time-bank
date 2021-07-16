# Generated by Django 3.2.3 on 2021-07-16 00:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_skillcategory'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='skill_categories',
            field=models.ManyToManyField(related_name='skill_categories', to='users.SkillCategory'),
        ),
    ]