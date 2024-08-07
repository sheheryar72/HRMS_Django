from django.urls import path
from .views import payroll_sheet_view, insert_data_from_all_ded_to_pay_sheet, get_payrollsheet

urlpatterns = [
    path('', payroll_sheet_view, name='payroll_sheet_view'),
    path('get_payrollsheet/<int:payroll_id>/', get_payrollsheet, name='get_payrollsheet'),
    path('insert_data_from_all_ded_to_pay_sheet/<int:payroll_id>/', insert_data_from_all_ded_to_pay_sheet, name='insert_data_from_all_ded_to_pay_sheet'),
]




