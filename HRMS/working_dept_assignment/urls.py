from django.urls import path
from .views import wda_view, getall_by_wdeptid, add_wda, update_wda

urlpatterns = [
    path('', wda_view, name='wda_view'),
    path('getall/<int:wdeptid>', getall_by_wdeptid, name='getall_by_wdeptid'),
    path('add', add_wda, name='add_wda'),
    path('update/<int:wdeptid>', update_wda, name='update_wda'),
]



