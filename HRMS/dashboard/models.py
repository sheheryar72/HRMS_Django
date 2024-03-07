from django.db import models

# Create your models here.

class  HR_GetUserMenuAndForms(models.Model):
    COID = models.IntegerField()
    CoName = models.CharField(max_length=50)
    User_ID = models.IntegerField()
    User_Name = models.CharField(max_length=50)
    FormID = models.IntegerField()
    FormDescr = models.CharField(max_length=100)
    ModuleID = models.IntegerField()
    ModuleDescr = models.CharField(max_length=50)
    MnuID = models.IntegerField()
    MnuDescr = models.CharField(max_length=50)
    MnuSubID = models.IntegerField()
    MnuSubDescr = models.CharField(max_length=50)
    FormSeq = models.IntegerField()
    FormStatusID = models.IntegerField()
    FormStatus = models.CharField(max_length=2)
    Status = models.BooleanField(default=True)
    
    class Meta:
        managed = False
        # db_table = ''
    def __str__(self):
        return self.FormDescr

# class GroupOfCompanies(models.Model):
#     CoID = models.AutoField(primary_key=True)
#     CoName = models.CharField(max_length=50, null=True)
#     Server_Name = models.CharField(max_length=50, null=True)
#     DB_Name = models.CharField(max_length=20, null=True)
#     db_UserName = models.CharField(max_length=50, null=True)
#     db_Password = models.CharField(max_length=50, null=True)
#     Active = models.BooleanField(default=True)
#     CoImage = models.CharField(max_length=50, null=True)
#     CoColor = models.CharField(max_length=50, null=True)
