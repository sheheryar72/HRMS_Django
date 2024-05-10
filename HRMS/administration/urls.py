from django.urls import path
from .views import getall_userprivileges, view_userprivileges, getall_groupofcompanies, getall_formDescription, add_userprivileges, view_userprivileges2, add_userprivileges2

urlpatterns = [
    path('userprivileges', view_userprivileges, name='view_userprivileges'),
    path('userprivileges2', view_userprivileges2, name='view_userprivileges'),
    path('userprivileges/getall/<int:userid>', getall_userprivileges, name='getall_userprivileges'),  
    path('company/getall', getall_groupofcompanies, name='getall_groupofcompanies'),  
    path('formdescription/getall', getall_formDescription, name='getall_formDescription'),  
    path('add', add_userprivileges, name='add_userprivileges'),  
    path('add2', add_userprivileges2, name='add_userprivileges'),  
]









