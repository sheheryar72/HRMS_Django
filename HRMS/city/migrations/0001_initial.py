# Generated by Django 5.0.1 on 2024-03-18 08:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='HR_City',
            fields=[
                ('CT_ID', models.AutoField(primary_key=True, serialize=False)),
                ('CT_Descr', models.CharField(blank=True, max_length=100)),
            ],
            options={
                'db_table': 'HR_CITY',
                'managed': False,
            },
        ),
    ]