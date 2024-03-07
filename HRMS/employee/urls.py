from django.urls import path
# from .views import get_all_employees
from .views import *
urlpatterns = [
    path('api/getall', get_all_employees, name='get_all_employees'),
    path('', Employees_view),
    path('api/getbyid/<int:emp_id>', get_Employees_by_id, name='get_Employees_by_id'),
    path('api/add', insert_Employees, name='insert_Employees'),
    path('api/update/<int:emp_id>', update_Employees, name='update_Employees'),
    path('api/delete/<int:emp_id>', delete_Employees, name='delete_Employees'),
]

