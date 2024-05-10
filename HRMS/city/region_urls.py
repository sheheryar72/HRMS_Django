from django.urls import path
from .region_view import *

urlpatterns = [
    path('', region_view),
    path('getall', getall, name='getall_region'),
    path('getbyid/<int:region_id>', getby_ID, name='get_region_by_id'),
    path('add', add, name='add_region'),
    path('update/<int:region_id>', update, name='update_region'),
    path('delete/<int:region_id>', delete, name='delete_region'),
]


