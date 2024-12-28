from django.db import models
from employee.models import HR_Employees 

class UserLogin(models.Model):
    User_ID = models.AutoField(primary_key=True)
    User_Emp_Code = models.CharField(max_length=10, blank=True, null=True)
    User_Name = models.CharField(max_length=200, blank=True, null=True)
    User_Password = models.CharField(max_length=50, blank=True, null=True)
    User_Post = models.CharField(max_length=200, blank=True, null=True)
    User_NICNo = models.CharField(max_length=50, blank=True, null=True)
    User_TelNo = models.CharField(max_length=50, blank=True, null=True)
    User_CellNo = models.CharField(max_length=50, blank=True, null=True)
    User_Email = models.CharField(max_length=50, blank=True, null=True)
    User_Status = models.BooleanField(blank=True, null=True)
    Emp_ID = models.ForeignKey(HR_Employees, to_field='Emp_ID', db_column='Emp_ID', null=True, blank=True,on_delete=models.CASCADE)

    class Meta:
        db_table = 'User_Login'
        managed = False

    def __str__(self):
        return self.User_Name


# from django.contrib.auth.models import AbstractUser

# class CustomUser(AbstractUser):
#     Emp_ID2 = models.IntegerField(null=True, blank=True)

#     def __str__(self):
#         return self.username

from django.contrib.auth.models import User
from employee.models import HR_Employees

class User_Profile(models.Model):
    Emp_ID_id = models.ForeignKey(HR_Employees, to_field='Emp_ID', db_column='Emp_ID_id', on_delete=models.CASCADE)
    user_id = models.OneToOneField(User, to_field='id', db_column='user_id', on_delete=models.CASCADE)
    Temp_Password = models.CharField(max_length=100, blank=True, null=True)
    Online = models.BooleanField(default=False)

    class Meta:
        managed = False
        db_table = 'User_Profile'
        #ordering = ['Emp_ID_id__Emp_Name']  # Sort by Emp_Name of HR_Employees
    
    def __str__(self):
        return str(self.user_id)
    
# class User_Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     # User_Emp_Code = models.CharField(max_length=10, blank=True, null=True)
#     User_Post = models.CharField(max_length=200, blank=True, null=True)
#     User_NICNo = models.CharField(max_length=50, blank=True, null=True)
#     User_TelNo = models.CharField(max_length=50, blank=True, null=True)
#     User_CellNo = models.CharField(max_length=50, blank=True, null=True)
#     Emp_ID = models.ForeignKey(HR_Employees, to_field='Emp_ID', db_column='Emp_ID', null=True, blank=True,on_delete=models.CASCADE)

#     class Meta:
#         managed = True
#         db_table = 'User_Profile'

#     def __str__(self):
#         return self.user.username




