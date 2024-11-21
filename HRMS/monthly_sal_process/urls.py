from django.urls import path
# from .views import getall_monthly_salary_mstr, monthlysalaryupdate_view, transfer_data_to_salary_process, getall_payrollperiod, salaryprocess_view, add_salary_update, update_salary_update, update_salary_Update, getll_emp_notin_salaryprocess, getall_payroll_element_notin_su, getll_master, getall_master_byid
from .views import *

urlpatterns = [
    path('', salaryprocess_view, name='salaryprocess_view'),
    path('monthlysalaryupdate/', monthlysalaryupdate_view, name='salaryprocess_view'),
    path('transfer_data_to_salary_process/<int:payroll_id>/<str:fuel_rate>/', transfer_data_to_salary_process, name='transfer_data_to_salary_process'),
    path('hr_monthly_salary_process/<int:payroll_id>/<str:fuel_rate>/', hr_monthly_salary_process, name='hr_monthly_salary_process'),
    path('execute_salary_process/<int:payroll_id>/<str:fuel_rate>/', execute_salary_process2, name='execute_salary_process'),
    path('getallmaster/<int:payroll_id>/', getall_master, name='getll_master'),
    # path('getallmaster/<int:payroll_id/', getall_master, name='getll_master'),
    path('getall_payrollperiod/', getall_payrollperiod, name='getall_payrollperiod'),
    path('get_active_period/', get_active_period, name='get_active_period'),
    path('get_salarystatus_distinct/', get_salarystatus_distinct, name='get_salarystatus_distinct'),
    path('addsalarymaster/', add_salary_update, name='add_salary_update'),
    path('updatesalary/<int:empupid>/<int:payroll_id>', update_salary_update, name='update_salary_update'),
    # path('addsalarydetail/', update_salary_Update, name='update_salary_Update'),
    path('getallemployee/', getll_emp_notin_salaryprocess, name='getll_emp_notin_salaryprocess'),
    path('getallmasterbyid/<int:empUpID>/<int:empID>/<int:payroll_id>/', getall_master_byid, name='getall_master_byid'),
    path('payrollelement/<int:empUpID>/<int:empID>/', getall_payroll_element_notin_su, name='getall_payroll_element_notin_su'),
    # path('getall_monthly_salary_mstr/', getall_monthly_salary_mstr, name='getall_monthly_salary_mstr'),
]




