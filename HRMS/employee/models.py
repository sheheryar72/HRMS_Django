# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from city.models import HR_City
from department.models import HR_Department
from designation.models import HR_Designation
from datetime import date
from datetime import datetime

# issue in venv so delete that file and make again

# to_field is the master table referecnce id
# db_column is the details table forngin key id

class TimeStampedModel(models.Model):
    insertedAt = models.DateField(auto_now_add=True)
    updatedAt = models.DateField(auto_now=True)

    class Meta:
        abstract = True

class HR_Employees(models.Model):
    Emp_ID = models.AutoField(primary_key=True, db_column='Emp_ID')   
    # Emp_ID = models.IntegerField(primary_key=True, db_column='Emp_ID')   
    HR_Emp_ID = models.IntegerField(db_column='HR_Emp_ID')  
    Emp_Name = models.CharField(db_column='Emp_Name', max_length=150, blank=True, null=True)  
    Father_Name = models.CharField(db_column='Father_Name', max_length=150, blank=True, null=True)  
    DateOfBirth = models.DateTimeField(db_column='DateOfBirth', blank=True, null=True)  
    Gender = models.CharField(db_column='Gender', max_length=10, blank=True, null=True)  
    Religion = models.CharField(db_column='Religion', max_length=15, blank=True, null=True)  
    # CT_ID = models.IntegerField(db_column='CT_ID', blank=True, null=True)  
    CT_ID = models.ForeignKey(HR_City, to_field='CT_ID', db_column='CT_ID', blank=True, null=True, on_delete=models.SET_NULL) 
    # CT_ID = models.ForeignKey(HR_City, db_column='CT_ID', blank=True, null=True, on_delete=models.CASCADE)
    CNIC_No = models.CharField(db_column='CNIC_No', max_length=15, blank=True, null=True)  
    Marital_Status = models.CharField(db_column='Marital_Status', max_length=10, blank=True, null=True)  
    Personal_Cell_No = models.CharField(db_column='Personal_Cell_No', max_length=12, blank=True, null=True)  
    Official_Cell_No = models.CharField(db_column='Official_Cell_No', max_length=12, blank=True, null=True)  
    Emergency_Cell_No = models.CharField(db_column='Emergency_Cell_No', max_length=12, blank=True, null=True)  
    Joining_Date = models.DateTimeField(db_column='Joining_Date', blank=True, null=True)  
    # Joining_Dsg_ID = models.IntegerField(db_column='Joining_Dsg_ID', blank=True, null=True)  
    Joining_Dsg_ID = models.ForeignKey(HR_Designation, to_field='DSG_ID', db_column='Joining_Dsg_ID', blank=True, null=True, on_delete=models.SET_NULL) 
    # Joining_Dept_ID = models.IntegerField(db_column='Joining_Dept_ID', blank=True, null=True)  
    Joining_Dept_ID = models.ForeignKey(HR_Department, to_field='Dept_ID', db_column='Joining_Dept_ID', blank=True, null=True, on_delete=models.SET_NULL) 
    Co_ID = models.IntegerField(db_column='Co_ID', blank=True, null=True)  
    Emp_Status = models.BooleanField(db_column='Emp_Status', blank=True, null=True)  
    Emp_ProfileImage = models.BinaryField(db_column='Emp_ProfileImage', blank=True, null=True)  
    Emp_Documents_File = models.BinaryField(db_column='Emp_Documents_File', blank=True, null=True)  
    # profileimage = models.ImageField(upload_to='profile/', default='employee/default.jpg')
    profileimage = models.ImageField(upload_to='profile/', default='profile/default.jpg')
    # mod_date = models.DateField(default=date.today)
    
    # New Fields
    Address = models.CharField(max_length=300, null=True, blank=True)
    Email = models.CharField(max_length=50, null=True, blank=True)
    CNIC_Issue_Date = models.DateField(null=True, blank=True)
    CNIC_Exp_Date = models.DateField(null=True, blank=True)
    Confirmation_Date = models.DateField(null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'HR_Employees'
    
    def __str__(self):
        return self.Emp_Name
    
class HR_Employees2(TimeStampedModel):
    Emp_Name = models.CharField(db_column='Emp_Name', max_length=150, blank=True, null=True)  
    Father_Name = models.CharField(db_column='Father_Name', max_length=150, blank=True, null=True)  

    class Meta:
        managed = True
        db_table = 'HR_Employees2'
    
    def __str__(self):
        return self.Emp_Name
    


