from django.urls import path
from .views import Department_view, get_all_department, get_department_by_id, insert_department, update_department, delete_department

urlpatterns = [
    path('', Department_view),
    path('getall', get_all_department, name='get_all_department'),
    path('getbyid/<int:department_id>', get_department_by_id, name='get_department_by_id'),
    path('add', insert_department, name='insert_department'),
    path('update/<int:department_id>', update_department, name='update_department'),
    path('delete/<int:department_id>', delete_department, name='delete_department'),
]




