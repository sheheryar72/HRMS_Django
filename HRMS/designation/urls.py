from django.urls import path
from .views import Designation_view, get_all_designation, get_designation_by_id, insert_designation, update_designation, delete_designation

urlpatterns = [
    path('', Designation_view),
    path('getall', get_all_designation, name='get_all_designation'),
    path('getbyid/<int:designation_id>', get_designation_by_id, name='get_designation_by_id'),
    path('add', insert_designation, name='insert_designation'),
    path('update/<int:designation_id>', update_designation, name='update_designation'),
    path('delete/<int:designation_id>', delete_designation, name='delete_designation'),
]

