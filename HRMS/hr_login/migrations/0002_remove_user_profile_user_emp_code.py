# Generated by Django 5.0.1 on 2024-05-02 10:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hr_login', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user_profile',
            name='User_Emp_Code',
        ),
    ]