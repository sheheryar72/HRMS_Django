from django.db import models
from employee.models import HR_Employees
from payroll_period.models import HR_PAYROLL_PERIOD
from payroll_element.models import HR_Payroll_Elements
from grade.models import HR_Grade
from department.models import HR_Department

class HR_Monthly_All_Ded(models.Model):
    Employee = models.ForeignKey(HR_Employees, db_column='Emp_ID', to_field='Emp_ID', on_delete=models.CASCADE)
    Period = models.ForeignKey(HR_PAYROLL_PERIOD, db_column='Payroll_ID', to_field='PAYROLL_ID', on_delete=models.CASCADE)
    Department = models.ForeignKey(HR_Department, db_column='Dept_ID', to_field='Dept_ID', on_delete=models.CASCADE)
    Basic_Salary_1 = models.FloatField(blank=True, null=True)
    Medical_Allowance_2 = models.FloatField(blank=True, null=True)
    Conveyance_Fixed_Allowance_3 = models.FloatField(blank=True, null=True)
    Overtime_Allowance_4 = models.FloatField(blank=True, null=True)
    House_Rent_Allowance_5 = models.FloatField(blank=True, null=True)
    Utilities_Allowance_6 = models.FloatField(blank=True, null=True)
    Meal_Allowance_7 = models.FloatField(blank=True, null=True)
    Arrears_8 = models.FloatField(blank=True, null=True)
    Bike_Maintainence_9 = models.FloatField(blank=True, null=True)
    Incentives_Tech_10 = models.FloatField(blank=True, null=True)
    Device_Reimbursment_11 = models.FloatField(blank=True, null=True)
    Communication_12 = models.FloatField(blank=True, null=True)
    Incentives_KPI_13 = models.FloatField(blank=True, null=True)
    Other_Allowance_14 = models.FloatField(blank=True, null=True)
    Loan_15 = models.FloatField(blank=True, null=True)
    Advance_Salary_16 = models.FloatField(blank=True, null=True)
    EOBI_17 = models.FloatField(blank=True, null=True)
    Income_Tax_18 = models.FloatField(blank=True, null=True)
    Absent_Days_19 = models.FloatField(blank=True, null=True)
    Device_Deduction_20 = models.FloatField(blank=True, null=True)
    Over_Utilization_Mobile_21 = models.FloatField(blank=True, null=True)
    Vehicle_Fuel_Deduction_22 = models.FloatField(blank=True, null=True)
    Pandamic_Deduction_23 = models.FloatField(blank=True, null=True)
    Late_Days_24 = models.FloatField(blank=True, null=True)
    Other_Deduction_25 = models.FloatField(blank=True, null=True)
    Mobile_Installment_26 = models.FloatField(blank=True, null=True)
    Food_Panda_27 = models.FloatField(blank=True, null=True)
    Conveyance_Liters_Allowance_28 = models.FloatField(blank=True, null=True)
    Leaves_29 = models.FloatField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'HR_Monthly_All_Ded'

    def __str__(self):
        return str(self.Basic_Salary_1)

# class HR_Monthly_All_Ded(models.Model):
#     Employee = models.ForeignKey(HR_Employees, db_column='Emp_ID', to_field='Emp_ID', on_delete=models.CASCADE)
#     Period = models.ForeignKey(HR_PAYROLL_PERIOD, db_column='Payroll_ID', to_field='PAYROLL_ID', on_delete=models.CASCADE)
#     Department = models.ForeignKey(HR_Department, db_column='Dept_ID', to_field='Dept_ID', on_delete=models.CASCADE)
#     Basic_Salary_1 = models.IntegerField(blank=True, null=True)
#     Medical_Allowance_2 = models.IntegerField(blank=True, null=True)
#     Conveyance_Allowance_3 = models.IntegerField(blank=True, null=True)
#     Overtime_Allowansce_4 = models.IntegerField(blank=True, null=True)
#     House_Rent_Allowanc_5 = models.IntegerField(blank=True, null=True)
#     Utilities_Allowance_6 = models.IntegerField(blank=True, null=True)
#     Meal_Allowance_7 = models.IntegerField(blank=True, null=True)
#     Arrears_8 = models.IntegerField(blank=True, null=True)
#     Bike_Maintainence_9 = models.IntegerField(blank=True, null=True)
#     Incentives_10 = models.IntegerField(blank=True, null=True)
#     Device_Reimbursment_11 = models.IntegerField(blank=True, null=True)
#     Communication_12 = models.IntegerField(blank=True, null=True)
#     Bonus_13 = models.IntegerField(blank=True, null=True)
#     Other_Allowance_14 = models.IntegerField(blank=True, null=True)
#     Loan_15 = models.IntegerField(blank=True, null=True)
#     Advance_Salary_16 = models.IntegerField(blank=True, null=True)
#     EOBI_17 = models.IntegerField(blank=True, null=True)
#     Income_Tax_18 = models.IntegerField(blank=True, null=True)
#     Absent_Days_19 = models.IntegerField(blank=True, null=True)
#     Device_Deduction_20 = models.IntegerField(blank=True, null=True)
#     Over_Utilizaton_Mobile_21 = models.IntegerField(blank=True, null=True)
#     Vehicle_or_Fuel_Deduction_22 = models.IntegerField(blank=True, null=True)
#     Pandamic_Deduction_23 = models.IntegerField(blank=True, null=True)
#     Late_Days_24 = models.IntegerField(blank=True, null=True)
#     Other_Deduction_25 = models.IntegerField(blank=True, null=True)
#     Mobile_Installment_26 = models.IntegerField(blank=True, null=True)
#     Food_Panda_27 = models.IntegerField(blank=True, null=True)

#     class Meta:
#         managed = True
#         db_table = 'HR_Monthly_All_Ded'

#     def __str__(self):
#         return str(self.Basic_Salary_1)

class HR_Element_Grade_Combination(models.Model):
    Combination_ID = models.AutoField(primary_key=True)
    Element_ID = models.ForeignKey(HR_Payroll_Elements, db_column='Element_ID', to_field='Element_ID', null=True, on_delete=models.CASCADE)
    Grade_ID = models.ForeignKey(HR_Grade, db_column='Grade_ID', to_field='Grade_ID', null=True, on_delete=models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = 'HR_Element_Grade_Combination'
    
    def __str__(self):
        return str(self.Combination_ID)

class HR_Emp_Salary_Grade_V(models.Model):
    # Emp_ID = models.IntegerField(primary_key=True)
    # Emp_Name = models.CharField(max_length=150)

    Emp_ID = models.AutoField(primary_key=True, db_column='Emp_ID')   
    Emp_Name = models.CharField(db_column='Emp_Name', max_length=150, blank=True, null=True)  
    HR_Emp_ID = models.IntegerField()
    Grade_ID = models.IntegerField()
    Grade_Descr = models.CharField(max_length=50)
    Dept_ID = models.IntegerField()

    class Meta:
        managed = False  
        db_table = 'HR_Emp_Salary_Grade_V'

    def __str__(self):
        return self.Emp_Name

