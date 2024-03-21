from django.db import models
from employee.models import HR_Employees
from payroll_period.models import HR_PAYROLL_PERIOD

class HR_Monthly_All_Ded(models.Model):
    Employee = models.ForeignKey(HR_Employees, db_column='Emp_ID', to_field='Emp_ID', on_delete=models.CASCADE)
    Period = models.ForeignKey(HR_PAYROLL_PERIOD, db_column='Payroll_Period_ID', to_field='ID', on_delete=models.CASCADE)
    Basic_Salary_01 = models.IntegerField()
    Medical_Allowance_02 = models.IntegerField()
    Conveyance_Allowance_03 = models.IntegerField()
    Overtime_Allowance_04 = models.IntegerField()
    House_Rent_Allowanc_05 = models.IntegerField()
    Utilities_Allowance_06 = models.IntegerField()
    Meal_Allowance_07 = models.IntegerField()
    Bike_Maintainence_08 = models.IntegerField()
    Device_Reimbursment_09 = models.IntegerField()
    Communication_10 = models.IntegerField()
    Bonus_11 = models.IntegerField()
    Other_Allowance_12 = models.IntegerField()
    Loan_13 = models.IntegerField()
    Advance_Salary_14 = models.IntegerField()
    EOBI_15 = models.IntegerField()
    Income_Tax_16 = models.IntegerField()
    Absent_Days_17 = models.IntegerField()
    Device_Deduction_18 = models.IntegerField()
    Over_Utilizaton_Mobile_19 = models.IntegerField()
    Vehicle_or_Fuel_Deduction_20 = models.IntegerField()
    Pandamic_Deduction_21 = models.IntegerField()
    Late_Days_22 = models.IntegerField()
    Other_Deduction_23 = models.IntegerField()
    Mobile_Installment_24 = models.IntegerField()
    Food_Panda_25 = models.IntegerField()
    Arrears_26 = models.IntegerField()
    Incentives_27 = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'HR_Monthly_All_Ded'

    def __str__(self):
        return str(self.Basic_Salary_01)


    


