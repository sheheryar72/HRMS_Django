from django.urls import path
from .views import Designation_view, get_all_designation, get_designation_by_id, insert_designation, update_designation, delete_designation

urlpatterns = [
    path('', Designation_view),
    path('api/getall', get_all_designation, name='get_all_designation'),
    path('api/getbyid/<int:designation_id>', get_designation_by_id, name='get_designation_by_id'),
    path('api/add', insert_designation, name='insert_designation'),
    path('api/update/<int:designation_id>', update_designation, name='update_designation'),
    path('api/delete/<int:designation_id>', delete_designation, name='delete_designation'),
]

