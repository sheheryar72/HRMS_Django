from django.urls import path
from .views import city_view, get_all_cities, get_city_by_id, insert_city, update_city, delete_city

urlpatterns = [
    path('', city_view),
    path('api/getall', get_all_cities, name='get_all_cities'),
    path('api/getbyid/<int:city_id>', get_city_by_id, name='get_city_by_id'),
    path('api/add', insert_city, name='insert_city'),
    path('api/update/<int:city_id>', update_city, name='update_city'),
    path('api/delete/<int:city_id>', delete_city, name='delete_city'),
]


