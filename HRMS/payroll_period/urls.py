from django.urls import path
from .views import payrollperiod_view, get_all_finYear, get_byid_finYear, add_finYear, delete_finYear, update_finYear, get_allpayrollperiod, update_month

urlpatterns = [
    path('', payrollperiod_view),
    path('api/getall', get_all_finYear, name='get_all_finYear'),
    path('api/get_byid_finYear/<int:id>', get_byid_finYear, name='get_byid_finYear'),
    path('api/add', add_finYear, name='add_finYear'),
    path('api/update/<int:id>', update_finYear, name='update_grade'),
    path('api/delete/<int:id>', delete_finYear, name='delete_finYear'),
    path('api/getallpayrollperiod/<int:id>', get_allpayrollperiod, name='get_allpayrollperiod'),
    path('api/updatemonth/<int:id>', update_month, name='upate_month'),
]

    