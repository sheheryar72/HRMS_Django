from django.db import models
from employee.models import HR_Employees
from payroll_element.models import HR_Payroll_Elements

class HR_Emp_Monthly_Sal_Mstr(models.Model):
    Emp_ID = models.ForeignKey(HR_Employees, on_delete=models.CASCADE)
    SalMonth = models.CharField(max_length=2)
    SalYear = models.CharField(max_length=4)
    MDAYS = models.IntegerField()
    WDAYS = models.IntegerField()
    DDAYS = models.IntegerField()
    SAL_CLOSED = models.BooleanField(default=False)
    Remarks = models.CharField(max_length=250)
    GrossSalary = models.FloatField()

    class Meta:
        managed = True
        db_table = 'HR_Emp_Monthly_Sal_Mstr'

class HR_Emp_Monthly_Sal_Dtl(models.Model):
    Emp_Up_ID = models.ForeignKey(HR_Emp_Monthly_Sal_Mstr, to_field='id', db_column='Emp_Up_ID', on_delete=models.CASCADE)
    Emp_ID = models.ForeignKey(HR_Employees, to_field='Emp_ID', db_column='Emp_ID', on_delete=models.CASCADE)
    Element_ID = models.ForeignKey(HR_Payroll_Elements, to_field='Element_ID', db_column='Element_ID' ,on_delete=models.CASCADE)
    Cal_Type = models.CharField(max_length=50)
    Cal_Value = models.FloatField()
    Amount = models.FloatField()

    class Meta:
        managed = True
        db_table = 'HR_Emp_Monthly_Sal_Dtl'


