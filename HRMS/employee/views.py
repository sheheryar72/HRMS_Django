from django.shortcuts import render
from django.db import connection
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import HR_Employees
from .serializers import HR_Employees_Serializer
from django.db.models import Max
from django.db import transaction
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

def Employees_view(request):
    print('Employees called')
    return render(request, 'employee.html')

@api_view(['GET'])
def get_all_employees(request):
    try:
        print('get_all_employees: ')
        employees = HR_Employees.objects.all()
        # employees = HR_Employees.objects.select_related('City').all()
        print('employees: ', employees)
        if not employees:
            return Response(status=status.HTTP_204_NO_CONTENT)

        serializer = HR_Employees_Serializer(employees, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def get_Employees_by_id(request, emp_id):
    try:
        try:
            Employees = HR_Employees.objects.get(pk=emp_id)
            print('id: ', emp_id)
            print('employees: ', Employees)
        except HR_Employees.DoesNotExist:
            return Response({'error': 'Employees not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = HR_Employees_Serializer(Employees)
        return Response(serializer.data, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# @api_view(['POST'])
# def insert_Employees(request):
#     try:
#         print('insert_Employees')
#         max_emp_id = HR_Employees.objects.aggregate(Max('Emp_ID'))
#         print('max_emp_id: ', max_emp_id['Emp_ID__max'])

#         max_emp_id_value = max_emp_id['Emp_ID__max']

#         print('max_emp_id_value: ', max_emp_id_value)

#         new_emp_id = max_emp_id_value + 1 if max_emp_id_value is not None else 1
#         request.data['Emp_ID'] = new_emp_id

#         serializer = HR_Employees_Serializer(data=request.data)

#         print('serializer: ', serializer)
#         # print('request.data: ', request.data)
#         if serializer.is_valid():
#             print('check valid:')
#             new_employee = serializer.save()
#             print('new_employee: ', new_employee)
#             serialized_data = serializer.data
#             return Response(serialized_data, status=status.HTTP_201_CREATED)

#         return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

#     except Exception as e:
#         return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# @api_view(['POST'])
# def insert_Employees(request):
#     try:
#         print('request.data: ', request.data)
#         print('profileimage: ', request.data.get('profileimage'))
#         serializer = HR_Employees_Serializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(data=serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#     except Exception as e:
#         return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(['POST'])
def insert_Employees(request):
    try:
        print('request.data: ', request.data)
        # Create a serializer instance with the request data
        serializer = HR_Employees_Serializer(data=request.data)

        # Check if the serializer is valid
        if serializer.is_valid():
            # Save the serializer without committing to database
            print('request data: ', request.data)
            employee_instance = serializer.save()


            # Handle the profileImage file upload
            if 'profileImage' in request.FILES:
                profile_image = request.FILES['profileImage']
                print('profile_image: ', profile_image)
                file_path = default_storage.save(f'profile/{profile_image.name}', ContentFile(profile_image.read()))
                employee_instance.profileimage = file_path

            # Save the employee instance with the updated profileimage field
            employee_instance.save()

            # Return a success response
            return Response(serializer.data, status=status.HTTP_200_OK)

        # Return a validation error response if the serializer is not valid
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        # Return a server error response if an exception occurs
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['PUT'])
def update_Employees(request, emp_id):
    try:

        print('emp_id: ', emp_id)
        print('request.data: ', request.data)

        Employees = HR_Employees.objects.get(pk=emp_id)
    except HR_Employees.DoesNotExist:
        return Response({'error': 'Employees not found'}, status=status.HTTP_404_NOT_FOUND)

    try:
        serializer = HR_Employees_Serializer(Employees, data=request.data, partial=True)
        if serializer.is_valid():
            updated_Employees = serializer.save()
            serialized_data = HR_Employees_Serializer(updated_Employees).data
            return Response(serialized_data, status=status.HTTP_200_OK)

        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['DELETE'])
def delete_Employees(request, emp_id):
    try:
        Employees = HR_Employees.objects.get(pk=emp_id)
    except HR_Employees.DoesNotExist:
        return Response({'error': 'Employees not found'}, status=status.HTTP_404_NOT_FOUND)

    try:
        Employees.delete()
        return Response({'message': 'Employees deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    