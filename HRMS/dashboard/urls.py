from django.urls import path
from .views import get_all_usermenuforms, dashboard_view


urlpatterns = [
    path('', dashboard_view, name='dashboard_view'),
    path('userform/', get_all_usermenuforms, name='get_all_usermenuforms'),
]
