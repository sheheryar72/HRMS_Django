from django.urls import path
from .region_view import *

urlpatterns = [
    path('', region_view),
    path('getall', get_all_regions, name='getall_region'),
    path('getbyid/<int:region_id>', get_region_by_id, name='get_region_by_id'),
    path('add', insert_region, name='add_region'),
    path('update/<int:region_id>', update_region, name='update_region'),
    path('delete/<int:region_id>', delete_region, name='delete_region'),
]


