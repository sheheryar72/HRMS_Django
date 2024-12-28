from django.db import models

# Create your models here.
class Salary_Slip(models.Model):
    Emp_Sl_ID = models.AutoField(primary_key=True)
    Emp_Sl_Date = models.DateTimeField(null=True)
    Emp_ID = models.IntegerField(null=True)
    HR_Emp_ID = models.IntegerField()
    Dsg_ID = models.IntegerField()
    DSG_Descr = models.CharField(max_length=100)
    Dept_ID = models.IntegerField()
    Dept_Descr = models.CharField(max_length=100)
    Grade_ID = models.IntegerField()
    Grade_Descr = models.CharField(max_length=100)
    Co_ID = models.IntegerField()
    Month_Days = models.FloatField()
    Ded_Days = models.FloatField()
    Working_Days = models.FloatField()
    Leave_Bal = models.FloatField()
    Element_ID = models.IntegerField()
    Element_Name = models.CharField(max_length=100)
    Amount = models.FloatField()
    Element_Type = models.CharField(max_length=100)
    Element_Category = models.CharField(max_length=100)

    class Meta:
        managed = False

    def __str__(self):
        return str(self.Emp_ID)
