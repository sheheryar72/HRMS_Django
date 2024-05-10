from django.urls import path
# from .views import get_all_employees
from .views import *
urlpatterns = [
    path('getall', get_all_employees, name='get_all_employees'),
    path('', Employees_view),
    path('getbyid/<int:emp_id>', get_Employees_by_id, name='get_Employees_by_id'),
    path('add', insert_Employees, name='insert_Employees'),
    path('update/<int:emp_id>', update_Employees, name='update_Employees'),
    path('delete/<int:emp_id>', delete_Employees, name='delete_Employees'),
]

