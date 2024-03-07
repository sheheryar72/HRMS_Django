from django.urls import path
from .views import *

urlpatterns = [
    path('', payrollelement, name='payrollelement'),
    path('api/getall/', getall, name='getall'),
    path('api/getbyid/<int:id>', getbyid, name='getbyid'),
    path('api/delete/<int:id>', delete, name='delete'),
    path('api/add/', add_payrollelement, name='add_payrollelement'),
    path('api/update/<int:id>', update_payrollelement, name='update_payrollelement'),
]









