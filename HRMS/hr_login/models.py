from django.db import models

class UserLogin(models.Model):
    User_ID = models.AutoField(primary_key=True)
    User_Emp_Code = models.CharField(max_length=10, blank=True)
    User_Name = models.CharField(max_length=200, blank=True)
    User_Password = models.CharField(max_length=50, blank=True)
    User_Post = models.CharField(max_length=200, blank=True, null=True)
    User_NICNo = models.CharField(max_length=50, blank=True, null=True)
    User_TelNo = models.CharField(max_length=50, blank=True, null=True)
    User_CellNo = models.CharField(max_length=50, blank=True, null=True)
    User_Email = models.CharField(max_length=50, blank=True, null=True)
    User_Status = models.BooleanField(blank=True)

    class Meta:
        db_table = 'User_Login'
        managed = False
        # using = 'erp_admin'  # Specify the database alias here
        #using = 'erp_admin'

    def __str__(self):
        return self.User_Name
