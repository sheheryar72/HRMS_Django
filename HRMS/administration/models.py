from django.db import models
from hr_login.models import UserLogin 

class FormDescription(models.Model):
    FormID = models.AutoField(primary_key=True)    
    FormDescr = models.CharField(max_length=50)    
    ModuleID = models.CharField(max_length=3)    
    ModuleDescr = models.CharField(max_length=50)    
    MnuID = models.CharField(max_length=3)    
    MnuDescr = models.CharField(max_length=50)    
    ModuleDescr = models.CharField(max_length=50)    
    MnuSubID = models.CharField(max_length=2)    
    MnuSubDescr = models.CharField(max_length=50)    
    FormSeq = models.CharField(max_length=5)    
    FormType = models.CharField(max_length=100)    

    class Meta:
        managed = False
        db_table = 'FormDescription'

    def __str__(self):
        return self.FormDescr

class GroupOfCompanies(models.Model):
    CoID = models.AutoField(primary_key=True)    
    CoName = models.CharField(max_length=50)    
    Server_Name = models.CharField(max_length=50)    
    DB_Name = models.CharField(max_length=20)    
    db_UserName = models.CharField(max_length=50)    
    db_Password = models.CharField(max_length=50)    
    Active = models.BooleanField()    
    CoImage = models.CharField(max_length=50)    
    CoColor = models.CharField(max_length=50, null=True)    

    class Meta:
        managed = False
        db_table = 'GroupOfCompanies'

    def __str__(self):
        return self.CoName

from django.contrib.auth.models import User
from hr_login.models import *

class User_Froms(models.Model):
    UF_ID = models.AutoField(primary_key=True)
    COID = models.IntegerField()
    # FormID = models.IntegerField()
    FormDescription = models.ForeignKey(FormDescription, to_field='FormID', db_column='FormID', null=True, on_delete=models.SET_NULL)
    # UserDetail = models.ForeignKey(UserLogin, to_field='User_ID', db_column='User_ID', null=True, on_delete=models.SET_NULL)
    UserProfile = models.ForeignKey(UserProfile, to_field='id', db_column='Profile_ID', on_delete=models.CASCADE)
    ModuleID = models.IntegerField()   
    MnuID = models.IntegerField()   
    MnuSubID = models.IntegerField()   
    # User_ID = models.IntegerField()  
    FormSeq = models.IntegerField()  
    FormStatusID = models.IntegerField()   
    FormStatus = models.CharField(max_length=2)    
    Status = models.BooleanField()    
    # FormDescription = models.OneToOneField(FormDescription, to_field='FormID', db_column='FormID', null=True, on_delete=models.SET_NULL)
    # FormDescription = models.ForeignKey(FormDescription, to_field='FormID', db_column='FormID', null=True, on_delete=models.SET_NULL)

    class Meta:
        managed = False
        db_table = 'User_Forms'

    def __str__(self):
        return str(self.UF_ID)

# class User_Froms(models.Model):
#     UF_ID = models.AutoField(primary_key=True)
#     COID = models.IntegerField()
#     User_ID = models.IntegerField()  
#     # FormID = models.IntegerField()
#     ModuleID = models.IntegerField()   
#     MnuID = models.IntegerField()   
#     MnuSubID = models.IntegerField()   
#     FormSeq = models.IntegerField() 
#     FormStatusID = models.IntegerField()   
#     FormStatus = models.CharField(max_length=2)    
#     Status = models.BooleanField()    
#     FormDescription = models.OneToOneField(FormDescription, to_field='FormID', db_column='FormID', null=True, on_delete=models.SET_NULL)
#     # FormDescription = models.ForeignKey(FormDescription, to_field='FormID', db_column='FormID', null=True, on_delete=models.SET_NULL)

#     class Meta:
#         managed = False
#         db_table = 'User_Forms'

#     def __str__(self):
#         return str(self.User_ID)
    





