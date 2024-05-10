from django.urls import path
from .views import *

urlpatterns = [
    path('', payrollelement, name='payrollelement'),
    path('getall/', getall, name='getall'),
    path('getbyid/<int:id>', getbyid, name='getbyid'),
    path('delete/<int:id>', delete, name='delete'),
    path('add/', add_payrollelement, name='add_payrollelement'),
    path('update/<int:id>', update_payrollelement, name='update_payrollelement'),
]









