from django.urls import path
from .views import salaryupdate_view, add_salary_update, update_salary_update, update_salary_Update, getll_emp_notin_salaryupdate, getall_payroll_element_notin_su, getll_master, getall_master_byid

urlpatterns = [
    path('', salaryupdate_view, name='salaryupdate_view'),
    path('getllmaster/', getll_master, name='getll_master'),
    path('addsalarymaster/', add_salary_update, name='add_salary_update'),
    path('updatesalary/<int:empupid>', update_salary_update, name='update_salary_update'),
    path('addsalarydetail/', update_salary_Update, name='update_salary_Update'),
    path('getallemployee/', getll_emp_notin_salaryupdate, name='getll_emp_notin_salaryupdate'),
    path('getallmasterbyid/<int:empUpID>/<int:empID>/', getall_master_byid, name='getall_master_byid'),
    path('payrollelement/<int:empUpID>/<int:empID>/', getall_payroll_element_notin_su, name='getall_payroll_element_notin_su'),
]




