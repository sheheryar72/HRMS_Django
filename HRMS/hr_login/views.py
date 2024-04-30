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
from employee.models import HR_Employees

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
    
@csrf_exempt
@api_view(['POST'])
def authenticate_user(request):
    try:
        # Get user credentials from the request
        username = request.data.get('username')
        password = request.data.get('password')

        print('username: ', username)
        print('password: ', password)

        # user = UserLogin.objects.filter(User_Name=username, User_Password=password)

        with connection.cursor() as cursor:
            cursor.execute("select User_ID, User_Name, User_Email, User_Password, User_Email, User_Status, Emp_ID from User_Login WHERE User_Name = %s AND User_Password = %s", [username, password])
            user = cursor.fetchone()

        print('user: ', user)

        if user is not None and user[1] == username and user[3] == password:  # Assuming User_Password is at index 3 in the result
            # Authentication successful
            print('user 6: ', user[6])
            emp_user = HR_Employees.objects.get(pk=user[6])
            print('emp_user: ', emp_user)
            data = {
                'Emp_ID': emp_user.Emp_ID,
                'Emp_Name': emp_user.Emp_Name,
                'HR_Emp_ID': emp_user.HR_Emp_ID,
                'Dep_ID': emp_user.Joining_Dept_ID.Dept_ID,
                'Dept_Descr': emp_user.Joining_Dept_ID.Dept_Descr
            }
            return JsonResponse({'data': data, 'message': 'Login successful!'})
        else:
            return JsonResponse({'error': 'Invalid username or password.'}, status=400)

    except Exception as e:
        return JsonResponse({'error': 'Authentication failed. Please check your credentials.'}, status=400)



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


@api_view(['GET'])
def getall_user(request):
    try:
        userlogin = UserLogin.objects.all()
        serializer = User_Login_Serializer(userlogin, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


