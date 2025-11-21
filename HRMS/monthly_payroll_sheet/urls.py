from django.urls import path
from .views import *

urlpatterns = [
    path('', payroll_sheet_view, name='payroll_sheet_view'),
    path('doj/', doj_report_view, name='doj_report_view'),
    path('process/', payroll_sheet_process_view, name='payroll_sheet_process_view'),
    path('execute_monthly_pay_sheet/<int:payroll_id>/', execute_monthly_pay_sheet_celery, name='execute_monthly_pay_sheet'),
    # path('get_payrollsheet/<int:payroll_id>/', get_payrollsheet, name='get_payrollsheet'),
    # path('insert_data_from_all_ded_to_pay_sheet/<int:payroll_id>/', insert_data_from_all_ded_to_pay_sheet, name='insert_data_from_all_ded_to_pay_sheet'),
    path('monthly-pay-sheet/<int:payroll_id>/', get_monthly_pay_sheet, name='get_monthly_pay_sheet'),
    # path('get_doj_report/<str:from_date>/<str:to_date>/', get_doj_report, name='get_doj_report'),
    path('get_doj_report/', get_doj_report, name='get_doj_report'),

]




