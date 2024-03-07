from django.urls import path
from .views import getall, add_leaves, update_leaves, delete, getbyid, leaves_view

urlpatterns = [
    path('', leaves_view, name='leaves_view'),
    path('api/getall/', getall, name='getall'),
    path('api/getbyid/<int:id>', getbyid, name='getbyid'),
    path('api/delete/<int:id>', delete, name='delete'),
    path('api/add', add_leaves, name='add_leaves'),
    path('api/update/<int:id>', update_leaves, name='update_leaves'),
]









