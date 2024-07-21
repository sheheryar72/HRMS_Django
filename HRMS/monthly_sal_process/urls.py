from django.urls import path
from .views import transfer_data_to_salary_process, getall_payrollperiod, salaryprocess_view, add_salary_update, update_salary_update, update_salary_Update, getll_emp_notin_salaryprocess, getall_payroll_element_notin_su, getll_master, getall_master_byid

urlpatterns = [
    path('', salaryprocess_view, name='salaryprocess_view'),
    path('transfer_data_to_salary_process/', transfer_data_to_salary_process, name='transfer_data_to_salary_process'),
    path('getllmaster/', getll_master, name='getll_master'),
    path('getall_payrollperiod/', getall_payrollperiod, name='getall_payrollperiod'),
    path('addsalarymaster/', add_salary_update, name='add_salary_update'),
    path('updatesalary/<int:empupid>', update_salary_update, name='update_salary_update'),
    path('addsalarydetail/', update_salary_Update, name='update_salary_Update'),
    path('getallemployee/', getll_emp_notin_salaryprocess, name='getll_emp_notin_salaryprocess'),
    path('getallmasterbyid/<int:empUpID>/<int:empID>/', getall_master_byid, name='getall_master_byid'),
    path('payrollelement/<int:empUpID>/<int:empID>/', getall_payroll_element_notin_su, name='getall_payroll_element_notin_su'),
]




