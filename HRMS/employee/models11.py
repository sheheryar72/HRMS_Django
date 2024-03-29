# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

# issue in venv so delete that file and make again

class HR_Employees(models.Model):
    emp_id = models.AutoField(db_column='Emp_ID', primary_key=True)   # Field name made lowercase.
    hr_emp_id = models.IntegerField(db_column='HR_Emp_ID')  # Field name made lowercase.
    emp_name = models.CharField(db_column='Emp_Name', max_length=150, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    father_name = models.CharField(db_column='Father_Name', max_length=150, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    dateofbirth = models.DateTimeField(db_column='DateOfBirth', blank=True, null=True)  # Field name made lowercase.
    gender = models.CharField(db_column='Gender', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    religion = models.CharField(db_column='Religion', max_length=15, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    ct_id = models.IntegerField(db_column='CT_ID', blank=True, null=True)  # Field name made lowercase.
    cnic_no = models.CharField(db_column='CNIC_No', max_length=15, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    marital_status = models.CharField(db_column='Marital_Status', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    personal_cell_no = models.CharField(db_column='Personal_Cell_No', max_length=12, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    official_cell_no = models.CharField(db_column='Official_Cell_No', max_length=12, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    emergency_cell_no = models.CharField(db_column='Emergency_Cell_No', max_length=12, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    joining_date = models.DateTimeField(db_column='Joining_Date', blank=True, null=True)  # Field name made lowercase.
    joining_dsg_id = models.IntegerField(db_column='Joining_Dsg_ID', blank=True, null=True)  # Field name made lowercase.
    joining_dept_id = models.IntegerField(db_column='Joining_Dept_ID', blank=True, null=True)  # Field name made lowercase.
    co_id = models.IntegerField(db_column='Co_ID', blank=True, null=True)  # Field name made lowercase.
    emp_status = models.BooleanField(db_column='Emp_Status', blank=True, null=True)  # Field name made lowercase.
    emp_profileimage = models.BinaryField(db_column='Emp_ProfileImage', blank=True, null=True)  # Field name made lowercase.
    emp_documents_file = models.BinaryField(db_column='Emp_Documents_File', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'HR_Employees'
    
    def __str__(self):
        return self.emp_name


