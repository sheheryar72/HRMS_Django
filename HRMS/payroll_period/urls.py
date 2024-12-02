from django.urls import path
# from .views import payrollperiod_view, get_all_finYear, get_byid_finYear, add_finYear, delete_finYear, update_finYear, get_allpayrollperiod, update_month
from .views import *

urlpatterns = [
    path('', payrollperiod_view),
    path('getall', get_all_finYear, name='get_all_finYear'),
    path('get_byid_finYear/<int:id>', get_byid_finYear, name='get_byid_finYear'),
    path('add', add_finYear, name='add_finYear'),
    path('update/<int:id>', update_finYear, name='update_grade'),
    path('delete/<int:id>', delete_finYear, name='delete_finYear'),
    path('getallpayrollperiod/<int:id>', get_allpayrollperiod, name='get_allpayrollperiod'),
    path('updatemonth/<int:id>', update_month, name='upate_month'),
    path('update_payroll_final_status/<int:id>/<str:payroll_type>/<int:payroll_status>', update_payroll_final_status, name='update_payroll_final_status'
)
]

    