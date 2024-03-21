from django.shortcuts import render
from django.db import connection
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import UserLogin
from django.http import JsonResponse
from django.http import HttpResponse
from rest_framework import status
from .serializers import User_Login_Serializer
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import check_password

def sheheryar_test2(request):
    return HttpResponse("Hi This is second request")  

def login_view(request):
    print('login called')
    #return render(request, template_name='index.html')
    return render(request, template_name='login.html')

def login2_view(request):
    print('login2 called')
    return render(request, template_name='login2.html')

def login3_view(request):
    print('login2 called')
    return render(request, template_name='dashboard.html')
    
# @csrf_exempt
# @api_view(['POST'])
# def authenticate_user(request):
#     try:
#         # Get user credentials from the request
#         username = request.data.get('username')
#         password = request.data.get('password')

#         # Authenticate user using Django's authenticate function with the specified database alias
#         user = authenticate(request, username=username, password=password, using='erp_admin')

#         print('username: ', username)
#         print('password: ', password)
#         print('user: ', user)

#         if user is not None:
#             # Login the user
#             login(request, user)
#             return JsonResponse({'message': 'Login successful!'})
#         else:
#             return JsonResponse({'error': 'Invalid email or password.'}, status=400)

#     except Exception as e:
#         return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@api_view(['POST'])
def authenticate_user(request):
    try:
        # Get user credentials from the request
        username = request.data.get('username')
        password = request.data.get('password')

        print('username: ', username)
        print('password: ', password)

        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM User_Login WHERE User_Name = %s AND User_Password = %s", [username, password])
            user = cursor.fetchone()

        print('user: ', user)

        if user is not None and user[2] == username and user[3] == password:  # Assuming User_Password is at index 3 in the result
            # Authentication successful
            return JsonResponse({'data': user[0], 'message': 'Login successful!'})
        else:
            return JsonResponse({'error': 'Invalid username or password.'}, status=400)

    except Exception as e:
        return JsonResponse({'error': 'Authentication failed. Please check your credentials.'}, status=400)


# @api_view(['POST'])
# def user_authenticate(request):
#     try:
#         userEmail = request.Post.get('username')
#         userPassword = request.Post.get('password')
#         with connection.cursor() as cursor:
#             cursor.execute("SELECT * FROM User_Login WHERE User_Email = %s AND User_Password = %s", [userEmail], [userPassword])
#             userData = cursor.fetchone()


#         return Response()

#     except Exception as e:
#         return Response({'error': str(e)}, status=500)


@api_view(['GET'])
def getall_user(request):
    try:
        userlogin = UserLogin.objects.all()
        serializer = User_Login_Serializer(userlogin, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


