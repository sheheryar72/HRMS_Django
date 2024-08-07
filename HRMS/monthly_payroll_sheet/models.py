from django.db import models
from employee.models import HR_Employees
from department.models import HR_Department
from payroll_period.models import HR_PAYROLL_PERIOD
from monthly_sal_process.models import HR_Emp_Monthly_Sal_Mstr

class HR_MONTHLY_PAY_SHEET(models.Model):
    # Emp_Up_ID = models.ForeignKey(HR_Emp_Monthly_Sal_Mstr, db_column='Emp_Up_ID', to_field='Emp_Up_ID', on_delete=models.CASCADE)
    Emp_Up_ID = models.IntegerField()
    Emp_ID = models.ForeignKey(HR_Employees, db_column='Emp_ID', to_field='Emp_ID', on_delete=models.CASCADE)
    Dept_ID = models.ForeignKey(HR_Department, db_column='Dept_ID', to_field='Dept_ID', on_delete=models.CASCADE)
    Payroll_ID = models.ForeignKey(HR_PAYROLL_PERIOD, db_column='Payroll_ID', to_field='PAYROLL_ID', on_delete=models.CASCADE)
    MDays = models.IntegerField()
    WDAYS = models.IntegerField()
    ADAYS = models.IntegerField()
    JLDAYS = models.IntegerField()
    Basic_Salary_1 = models.IntegerField(blank=True, null=True)
    Medical_Allowance_2 = models.IntegerField(blank=True, null=True)
    Conveyance_Allowance_3 = models.IntegerField(blank=True, null=True)
    Overtime_Allowansce_4 = models.IntegerField(blank=True, null=True)
    House_Rent_Allowanc_5 = models.IntegerField(blank=True, null=True)
    Utilities_Allowance_6 = models.IntegerField(blank=True, null=True)
    Meal_Allowance_7 = models.IntegerField(blank=True, null=True)
    Arrears_8 = models.IntegerField(blank=True, null=True)
    Bike_Maintainence_9 = models.IntegerField(blank=True, null=True)
    Incentives_10 = models.IntegerField(blank=True, null=True)
    Device_Reimbursment_11 = models.IntegerField(blank=True, null=True)
    Communication_12 = models.IntegerField(blank=True, null=True)
    Bonus_13 = models.IntegerField(blank=True, null=True)
    Other_Allowance_14 = models.IntegerField(blank=True, null=True)
    Loan_15 = models.IntegerField(blank=True, null=True)
    Advance_Salary_16 = models.IntegerField(blank=True, null=True)
    EOBI_17 = models.IntegerField(blank=True, null=True)
    Income_Tax_18 = models.IntegerField(blank=True, null=True)
    Absent_Days_19 = models.IntegerField(blank=True, null=True)
    Device_Deduction_20 = models.IntegerField(blank=True, null=True)
    Over_Utilizaton_Mobile_21 = models.IntegerField(blank=True, null=True)
    Vehicle_or_Fuel_Deduction_22 = models.IntegerField(blank=True, null=True)
    Pandamic_Deduction_23 = models.IntegerField(blank=True, null=True)
    Late_Days_24 = models.IntegerField(blank=True, null=True)
    Other_Deduction_25 = models.IntegerField(blank=True, null=True)
    Mobile_Installment_26 = models.IntegerField(blank=True, null=True)
    Food_Panda_27 = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'HR_MONTHLY_PAY_SHEET'

    def __str__(self):
        return str(self.Emp_ID.Emp_Name)
    