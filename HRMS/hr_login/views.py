from django.shortcuts import render, redirect
from django.db import connection
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import UserLogin, User_Profile
from django.http import JsonResponse
from django.http import HttpResponse
from rest_framework import status
from .serializers import User_Login_Serializer
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import check_password
from employee.models import HR_Employees
from django.contrib.auth import login as auth_login
# from profile import Profile
from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.models import Token

def staff_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        
        if not request.user.is_authenticated:
            logout(request)
            response = redirect('login_view')
            # Delete the authentication-related cookies
            response.delete_cookie('sessionid')
            response.delete_cookie('csrftoken')
            return response

        if not (request.user.is_superuser or request.user.is_staff):
            logout(request)
            response = redirect('login_view')
            response.delete_cookie('sessionid') 
            response.delete_cookie('csrftoken')
            return response

        return view_func(request, *args, **kwargs)
    
    return _wrapped_view

def sheheryar_test2(request):
    return HttpResponse("Hi This is second request")  

def login_view(request):
    print('login called')
    #return render(request, template_name='index.html')
    return render(request, template_name='login.html')

def login2_view(request):
    print('login2 called')
    return render(request, template_name='login2.html')

@csrf_exempt
@api_view(['POST'])
def login3_view(request):
    print('login2 called')
    return render(request, template_name='dashboard.html')
    
# @csrf_exempt
# @api_view(['POST'])
# @permission_classes([AllowAny])
# def authenticate_user(request):
#     try:
#         # Get user credentials from the request
#         username = request.data.get('username')
#         password = request.data.get('password')

#         print('username: ', username)
#         print('password: ', password)

#         # user = UserLogin.objects.filter(User_Name=username, User_Password=password)

#         with connection.cursor() as cursor:
#             cursor.execute("select User_ID, User_Name, User_Email, User_Password, User_Email, User_Status, Emp_ID from User_Login WHERE User_Name = %s AND User_Password = %s", [username, password])
#             user = cursor.fetchone()


#         if user is not None and user[1] == username and user[3] == password:  # Assuming User_Password is at index 3 in the result
#             # Authentication successful
#             print('user 6: ')
#             # emp_user = HR_Employees.objects.get(pk=user[6])
#             # print('emp_user: ', emp_user)
#             # data = {
#             #     'Emp_ID': emp_user.Emp_ID,
#             #     'Emp_Name': emp_user.Emp_Name,
#             #     'HR_Emp_ID': emp_user.HR_Emp_ID,
#             #     'Dep_ID': emp_user.Joining_Dept_ID.Dept_ID,
#             #     'Dept_Descr': emp_user.Joining_Dept_ID.Dept_Descr
#             # }
#             return JsonResponse({'data': user, 'message': 'Login successful!'})
#         else:
#             return JsonResponse({'error': 'Invalid username or password.'}, status=400)

#     except Exception as e:
#         return JsonResponse({'error': 'Authentication failed. Please check your credentials.'}, status=400)


@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def authenticate_user2(request):
    try:
        username = request.data.get('username')
        password = request.data.get('password')

        print('authenticate_user2 request:', request.data)

        if not username or not password:
            return JsonResponse({'error': 'Both username and password are required.'}, status=400)

        user = authenticate(username=username, password=password)
        
        print('user: ', user)

        if user is not None:
            login(request, user)

        # token, created = Token.objects.get_or_create(user=user)
        # print('token: ', token)

        if user is not None:
            auth_login(request, user)
            user_profile = User_Profile.objects.filter(user_id__username=username).first()

            print('user_profile user_profile: ', user_profile)

            if user_profile:
                # print('user_profile:', user_profile)
                # print('user_profile.Emp_ID_id:', user_profile.Emp_ID_id.Emp_ID)
                # print('user_profile.Emp_ID_id.Email:', user_profile.Emp_ID_id.Email)
                # print('user_profile.Emp_ID_id.Joining_Dept_ID:', user_profile.Emp_ID_id.Joining_Dept_ID)
                # print('user_profile.Emp_ID_id.Joining_Dept_ID.Dept_ID:', user_profile.Emp_ID_id.Joining_Dept_ID.Dept_ID)
                # print('user_profile.Emp_ID_id.Joining_Dept_ID.Dept_Descr:', user_profile.Emp_ID_id.Joining_Dept_ID.Dept_Descr)
                # print('user_profile.Emp_ID_id.Emp_ID:', user_profile.Emp_ID_id.Emp_ID)
                # print('user_profile.Emp_ID_id.Emp_Name:', user_profile.Emp_ID_id.Emp_Name)

                data = {
                    'Profile_ID': user_profile.id,
                    'token': None
                    # 'token': token.key if token else None
                    # 'Email': user_profile.Emp_ID_id.Email,
                    # 'Dept_ID': user_profile.Emp_ID_id.Joining_Dept_ID.Dept_ID,
                    # 'Dept_Descr': user_profile.Emp_ID_id.Joining_Dept_ID.Dept_Descr,
                    # 'Emp_ID': user_profile.Emp_ID_id.Emp_ID,
                    # 'Emp_Name': user_profile.Emp_ID_id.Emp_Name,
                }
                print('user_profile data:', data)

                return JsonResponse({'data': data, 'message': 'Login successful!'})
            else:
                return JsonResponse({'error': 'User profile not found.'}, status=400)
        else:
            return JsonResponse({'error': 'Invalid username or password.'}, status=400)

    except Exception as e:
        print('Exception:', e)
        return JsonResponse({'error': 'Authentication failed. Please check your credentials.'}, status=400)

@csrf_exempt
# @api_view(['GET'])
# @permission_classes([AllowAny])
def signout_user(request):
    print('signout_user')
    logout(request)
    response = redirect('login_view')
    response.delete_cookie('sessionid')
    response.delete_cookie('csrftoken')
    return response


# @csrf_exempt
# @api_view(['POST'])
# def authenticate_user(request):
#     try:
#         # Get user credentials from the request
#         username = request.data.get('username')
#         password = request.data.get('password')

#         print('username: ', username)
#         print('password: ', password)

#         # Check if the user exists
#         # user = UserLogin.objects.filter(User_Name=username, User_Password=password).first()
#         user = UserLogin.objects.first()

#         print('user: ', user)

#         if user is not None:
#             # Authentication successful
#             return JsonResponse({'data': user.id, 'message': 'Login successful!'})
#         else:
#             return JsonResponse({'error': 'Invalid username or password.'}, status=400)

#     except Exception as e:
#         return JsonResponse({'error': 'Authentication failed. Please check your credentials.'}, status=400)







# @csrf_exempt
# @api_view(['POST'])
# def authenticate_user(request):
#     try:
#         # Get user credentials from the request
#         username = request.data.get('username')
#         password = request.data.get('password')

#         print('username: ', username)
#         print('password: ', password)

#         user = UserLogin.objects.filter(User_Name=username, User_Password=password)

#         # with connection.cursor() as cursor:
#         #     cursor.execute("SELECT * FROM User_Login WHERE User_Name = %s AND User_Password = %s", [username, password])
#         #     user = cursor.fetchone()

#         print('user: ', user)

#         if user is not None and user[0].User_Name == username and user[0].User_Password == password:  # Assuming User_Password is at index 3 in the result
#             # Authentication successful
#             # login_user = HR_Employees.objects.filter(Emp_ID=user[0])
#             return JsonResponse({'data': user, 'message': 'Login successful!'})
#         else:
#             return JsonResponse({'error': 'Invalid username or password.'}, status=400)

#     except Exception as e:
#         return JsonResponse({'error': 'Authentication failed. Please check your credentials.'}, status=400)


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

from django.contrib.auth.models import User

@api_view(['GET'])
def getall_user(request):
    try:
        # userlogin = UserLogin.objects.all()
        # serializer = User_Login_Serializer(userlogin, many=True)
        all_users = User.objects.all()
        data = []
        for user in all_users:
            data.append({
            'id': user.id,
            'username': user.username
            }
            ) 

        return Response(data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


