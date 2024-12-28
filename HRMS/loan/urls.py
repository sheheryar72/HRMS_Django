from django.urls import path
from .views import *

urlpatterns = [
    path('', loan_view, name='loan_view'),
    path('getall', loan_list, name='loan_list'),
    path('getbyid/<int:pk>', loan_byid, name='loan_byid'),
    path('delete/<int:pk>', delete_loan, name='delete_loan'),
    path('add', add_loan, name='add_loan'),
    path('update/<int:pk>', update_loan, name='update_loan'),
]









