# Generated by Django 5.0.1 on 2024-04-03 07:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('grade', '0001_initial'),
        ('monthly_all_ded', '0005_rename_hr_payroll_element_grade_hr_payroll_grade_combination'),
        ('payroll_element', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='HR_Payroll_Grade_Combination',
            new_name='HR_Element_Grade',
        ),
    ]
