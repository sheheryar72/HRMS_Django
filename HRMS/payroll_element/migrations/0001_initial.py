# Generated by Django 5.0.1 on 2024-03-18 08:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='HR_Payroll_Elements',
            fields=[
                ('Element_ID', models.AutoField(primary_key=True, serialize=False)),
                ('Element_Name', models.CharField(max_length=50)),
                ('Element_Type', models.CharField(max_length=50)),
                ('Element_Category', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'HR_Payroll_Elements',
                'managed': False,
            },
        ),
    ]
