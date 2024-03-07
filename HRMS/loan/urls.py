from django.urls import path
from .views import *

urlpatterns = [
    path('', loan_view, name='loan_view'),
    path('api/getall', loan_list, name='loan_list'),
    path('api/getbyid/<int:pk>', loan_byid, name='loan_byid'),
    path('api/delete/<int:pk>', delete_loan, name='delete_loan'),
    path('api/add', add_loan, name='add_loan'),
    path('api/update/<int:pk>', update_loan, name='update_loan'),
]









