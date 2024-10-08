from django.urls import path, include
from .views import Index, getAll_W_Dept_By_DeptID, getAll_Assigned_Dept, getAll_W_Dept_By_W_DeptID, Insert_Monthly_PE, get_current_pp, export_template, Insert_from_excel

urlpatterns = [
    path('', Index, name='Index'),
    path('getall_dept_element/<int:W_DeptID>/<int:DeptID>/<int:Payroll_ID>', getAll_W_Dept_By_DeptID, name='getAll_W_Dept_By_DeptID'),
    path('getall_w_dept_element/<int:W_DeptID>', getAll_W_Dept_By_W_DeptID, name='getAll_W_Dept_By_W_DeptID'),
    path('getall_dept/<int:DeptID>', getAll_Assigned_Dept, name='getAll_Assigned_Dept'),
    path('insert/', Insert_Monthly_PE, name='Insert_Monthly_PE'),
    path('Insert_from_excel/', Insert_from_excel, name='Insert_from_excel'),
    path('current_payrollperiod/', get_current_pp, name='get_current_pp'),
    path('export_template/<int:ID>', export_template, name='export_template'),
]






























