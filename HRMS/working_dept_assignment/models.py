from django.db import models
from department.models import HR_Department
from payroll_element.models import HR_Payroll_Elements

class HR_W_All_Ded_Department(models.Model):
    ID = models.AutoField(primary_key=True)
    W_All_Ded_ID = models.IntegerField(null=True)
    W_All_Ded_Dept_ID = models.ForeignKey(HR_Department, db_column='W_All_Ded_Dept_ID', to_field='Dept_ID', on_delete=models.CASCADE, related_name='W_Dept_ID')
    W_All_Ded_Element_ID = models.ForeignKey(HR_Payroll_Elements, to_field='Element_ID', db_column='W_All_Ded_Element_ID', on_delete=models.CASCADE)
    Dept_ID = models.ForeignKey(HR_Department, db_column='Dept_ID', to_field='Dept_ID', on_delete=models.CASCADE, related_name='Assigned_Dept_ID')
    
    class Meta:
        managed = False
        db_table = 'HR_W_All_Ded_Department'
    
    def __str__(self):
        return str(self.ID)
