# Generated by Django 5.0.1 on 2024-04-26 07:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monthly_all_ded', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='HR_Emp_Salary_Grade_V',
            fields=[
                ('Emp_ID', models.AutoField(db_column='Emp_ID', primary_key=True, serialize=False)),
                ('Emp_Name', models.CharField(blank=True, db_column='Emp_Name', max_length=150, null=True)),
                ('HR_Emp_ID', models.IntegerField()),
                ('Grade_ID', models.IntegerField()),
                ('Grade_Descr', models.CharField(max_length=50)),
                ('Dept_ID', models.IntegerField()),
            ],
            options={
                'db_table': 'HR_Emp_Salary_Grade_V',
                'managed': False,
            },
        ),
    ]
