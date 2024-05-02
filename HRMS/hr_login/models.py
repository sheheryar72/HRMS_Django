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

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    Emp_ID = models.CharField(max_length=100)

    class Meta:
        managed = True
        db_table = 'User_Profile'

    def __str__(self):
        return self.user.username

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




