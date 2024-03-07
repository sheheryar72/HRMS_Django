from django.db import models
from payroll_period.models import HR_FinYearMstr
from employee.models import HR_Employees

class HR_Loans(models.Model):
    Loan_ID = models.AutoField(primary_key=True)
    Loan_Date = models.DateTimeField()
    Loan_Type = models.CharField(max_length=30)
    FYID = models.ForeignKey(HR_FinYearMstr, db_column='FYID', to_field='FYID', on_delete=models.CASCADE)
    Emp_ID = models.ForeignKey(HR_Employees, db_column='Emp_ID', to_field='Emp_ID', on_delete=models.CASCADE)
    Loan_Amount = models.FloatField()
    Loan_Ded_Amt = models.FloatField()
    Loan_Ded_NoofMnth = models.FloatField()
    Remarks = models.CharField(max_length=50)
    Loan_Status = models.BooleanField()
    Previous_Ded_Amount = models.FloatField()

    class Meta:
        managed = False
        db_table = 'HR_Loans'

    def __str__(self):
        return str(self.Loan_ID)


