from django.db import models
from employee.models import HR_Employees
from department.models import HR_Department
from designation.models import HR_Designation
from grade.models import HR_Grade
from payroll_element.models import HR_Payroll_Elements

class HR_Emp_Sal_Update_Mstr(models.Model):
    Emp_Up_ID = models.AutoField(primary_key=True)
    Emp_Up_Date = models.DateTimeField(auto_now_add=True)
    Emp_Category = models.CharField(max_length=100)
    Marital_Status = models.CharField(max_length=50)
    No_of_Children = models.IntegerField(null=True, blank=True)
    Co_ID = models.IntegerField()
    GrossSalary = models.FloatField()
    Remarks = models.CharField(max_length=200, null=True, blank=True)
    Emp_ID = models.ForeignKey(HR_Employees, db_column='Emp_ID', to_field='Emp_ID', on_delete=models.CASCADE)
    HR_Emp_ID = models.IntegerField()
    Grade_ID = models.ForeignKey(HR_Grade, db_column='Grade_ID', to_field='Grade_ID', on_delete=models.DO_NOTHING)
    Dsg_ID = models.ForeignKey(HR_Designation, db_column='Dsg_ID', to_field='DSG_ID', on_delete=models.CASCADE)
    Dept_ID = models.ForeignKey(HR_Department, db_column='Dept_ID', to_field='Dept_ID', on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'HR_Emp_Sal_Update_Mstr'

    def __str__(self):
        return str(self.Emp_Up_ID)

class HR_Emp_Sal_Update_Dtl(models.Model):
    ID = models.AutoField(primary_key=True)
    Emp_Up_ID = models.ForeignKey(HR_Emp_Sal_Update_Mstr, db_column='Emp_Up_ID', to_field='Emp_Up_ID', on_delete=models.CASCADE)
    Amount = models.FloatField()
    # Element_ID = models.IntegerField()
    Element_ID = models.ForeignKey(HR_Payroll_Elements, db_column='Element_ID', to_field='Element_ID', on_delete=models.CASCADE)
    Element_Type = models.CharField(max_length=10)
    Element_Category = models.CharField(max_length=10)
    Emp_ID = models.ForeignKey(HR_Employees, db_column='Emp_ID', to_field='Emp_ID', on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'HR_Emp_Sal_Update_Dtl'

    def __str__(self):
        return str(self.Emp_Up_ID)
