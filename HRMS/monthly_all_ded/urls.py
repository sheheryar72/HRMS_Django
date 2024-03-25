from django.urls import path, include
from .views import Index, getAll_W_Dept_By_DeptID, getAll_Assigned_Dept, getAll_W_Dept_By_W_DeptID

urlpatterns = [
    path('', Index, name='Index'),
    path('getall_dept_element/<int:W_DeptID>/<int:DeptID>', getAll_W_Dept_By_DeptID, name='getAll_W_Dept_By_DeptID'),
    path('getall_w_dept_element/<int:W_DeptID>', getAll_W_Dept_By_W_DeptID, name='getAll_W_Dept_By_W_DeptID'),
    path('getall_dept/<int:DeptID>', getAll_Assigned_Dept, name='getAll_Assigned_Dept'),
]






























