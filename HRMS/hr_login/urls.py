from django.urls import path
from .views import login_view, login2_view, login3_view, authenticate_user, sheheryar_test2, getall_user

urlpatterns = [
    # path('', sheheryar_test2, name='sheheryar_test2'),
    path('', login_view, name='login_view'),
    path('login2/', login2_view, name='login2_view'),
    path('login3/', login3_view, name='login3_view'),
    path('authenticate/', authenticate_user, name='authenticate_user'),
    path('api/getalluser/', getall_user, name='getall_user'),
]


