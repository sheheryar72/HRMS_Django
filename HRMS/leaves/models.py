from django.db import models
from payroll_period.models import HR_FinYearMstr
from employee.models import HR_Employees

class HR_Leaves(models.Model):
    Leaves_ID = models.AutoField(primary_key=True)
    FYID = models.ForeignKey(HR_FinYearMstr, db_column='FYID', to_field='FYID', on_delete=models.CASCADE)
    Emp_ID = models.ForeignKey(HR_Employees, db_column='Emp_ID', to_field='Emp_ID', on_delete=models.CASCADE)
    EL_OP = models.IntegerField()
    CL = models.IntegerField()
    SL = models.IntegerField()
    EL = models.IntegerField()
    EGL = models.IntegerField()
    EL_OP = models.IntegerField()
    LA_CL = models.IntegerField()
    LA_SL = models.IntegerField()
    LA_EL_OP = models.IntegerField()
    LA_EL = models.IntegerField()
    LA_EGL = models.IntegerField()
    Tot_LA = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'HR_Leaves'
        app_label = 'HR_Leaves'

    def __str__(self):
        return str(self.Leave_ID)
