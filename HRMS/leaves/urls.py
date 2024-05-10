from django.urls import path
from .views import getall, add_leaves, update_leaves, delete, getbyid, leaves_view

urlpatterns = [
    path('', leaves_view, name='leaves_view'),
    path('getall/', getall, name='getall'),
    path('getbyid/<int:id>', getbyid, name='getbyid'),
    path('delete/<int:id>', delete, name='delete'),
    path('add', add_leaves, name='add_leaves'),
    path('update/<int:id>', update_leaves, name='update_leaves'),
]









