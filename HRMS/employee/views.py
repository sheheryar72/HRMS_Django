from django.shortcuts import render
from django.db import connection
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from .models import HR_Employees, GroupOfCompanies, GroupOfCompaniesSerializer
from .serializers import HR_Employees_Serializer
from django.db.models import Max
from django.db import transaction
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import AllowAny
from django.utils import timezone
from datetime import datetime
from city.models import *
from designation.models import *
from department.models import *
from rest_framework import generics

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
    

# @api_view(['POST'])
# @csrf_exempt
@api_view(['POST'])
# @permission_classes([AllowAny])

def insert_employee(request):
    try:
        print('insert_employee called!')
        emp_data = request.data
        print('emp_data: ', emp_data)

        # Create a new employee instance
        employee = HR_Employees()

        # Map all the fields from the request data with default values
        employee.HR_Emp_ID = emp_data.get('HR_Emp_ID', None)
        employee.Emp_Name = emp_data.get('Emp_Name', '')
        employee.Father_Name = emp_data.get('Father_Name', '')
        employee.Address = emp_data.get('Address', '')
        employee.Emergency_Cell_No = emp_data.get('Emergency_Cell_No', '')
        employee.Personal_Cell_No = emp_data.get('Personal_Cell_No', '')
        employee.Official_Cell_No = emp_data.get('Official_Cell_No', '')
        employee.Email = emp_data.get('Email', '')
        employee.TEL_EXT = emp_data.get('TEL_EXT', '')
        employee.Gender = emp_data.get('Gender', '')
        employee.Marital_Status = emp_data.get('Marital_Status', '')
        employee.CNIC_No = emp_data.get('CNIC_No', '')
        employee.Religion = emp_data.get('Religion', '')
        employee.Co_ID = emp_data.get('Co_ID', 1)  # Default value for Co_ID

        # Handle foreign keys with default values
        ct_id = emp_data.get('CT_ID')
        if ct_id:
            employee.CT_ID = HR_City.objects.get(pk=ct_id)

        joining_dsg_id = emp_data.get('Joining_Dsg_ID')
        if joining_dsg_id:
            employee.Joining_Dsg_ID = HR_Designation.objects.get(pk=joining_dsg_id)

        joining_dept_id = emp_data.get('Joining_Dept_ID')
        if joining_dept_id:
            employee.Joining_Dept_ID = HR_Department.objects.get(pk=joining_dept_id)

        # employee.Emp_Status = emp_data.get('Emp_Status', True)
        
        # Handle date fields
        confirmation_date = emp_data.get('Confirmation_Date')
        if confirmation_date:
            employee.Confirmation_Date = timezone.datetime.strptime(confirmation_date, "%Y-%m-%d").date()
        
        cnic_issue_date = emp_data.get('CNIC_Issue_Date')
        if cnic_issue_date:
            employee.CNIC_Issue_Date = timezone.datetime.strptime(cnic_issue_date, "%Y-%m-%d").date()

        cnic_exp_date = emp_data.get('CNIC_Exp_Date')
        if cnic_exp_date:
            employee.CNIC_Exp_Date = timezone.datetime.strptime(cnic_exp_date, "%Y-%m-%d").date()

        date_of_birth = emp_data.get('DateOfBirth')
        if date_of_birth:
            employee.DateOfBirth = timezone.datetime.strptime(date_of_birth, "%Y-%m-%d").date()

        # Handle profile image (if required)
        # if 'ProfileImage' in request.FILES:
        #     profile_image = request.FILES['ProfileImage']
        #     ext = profile_image.name.split('.')[-1]  # Get the file extension
        #     profile_image_name = f"{employee.Emp_ID}.{ext}"  # Construct the new filename
        #     # Save new profile image with the empid name
        #     employee.ProfileImage.save(profile_image_name, profile_image, save=False)

        employee.save()

        emp_serializer = HR_Employees_Serializer(employee)
        return Response(emp_serializer.data, status=201)

    except Exception as e:
        return Response({'message': str(e)}, status=500)

# @api_view(['PUT'])
# def update_employee(request, emp_id):
#     print('update request data: ', request.data)
#     try:
#         employee = HR_Employees.objects.get(pk=emp_id)
#     except HR_Employees.DoesNotExist:
#         return Response({'error': 'Employee not found'}, status=status.HTTP_404_NOT_FOUND)

#     try:
#         # Use partial=True to update only provided fields
#         serializer = HR_Employees_Serializer(employee, data=request.data, partial=True)

#         if serializer.is_valid():
#             updated_employee = serializer.save()

#             # Handle file uploads separately if needed
#             # if 'profileImage' in request.FILES:
#             #     employee.profileimage = request.FILES['profileImage']
#             employee.save()

#             return Response(serializer.data, status=status.HTTP_200_OK)

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     except Exception as e:
#         return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    


@api_view(['POST'])
def update_employee(request, emp_id):
    try:
        emp_data = request.data
        if emp_id is None:
            return Response({'message': 'Bad request'}, status=400)

        employee = HR_Employees.objects.filter(Emp_ID=emp_id).first()

        if employee is None:
            return Response({'message': 'Employee not found'}, status=404)

        print('emp_data: ', emp_data)

        # Map all the fields from the request data
        employee.Emp_Name = emp_data.get('Emp_Name', employee.Emp_Name)
        employee.Father_Name = emp_data.get('Father_Name', employee.Father_Name)
        employee.Address = emp_data.get('Address', employee.Address)
        employee.Emergency_Cell_No = emp_data.get('Emergency_Cell_No', employee.Emergency_Cell_No)
        employee.Personal_Cell_No = emp_data.get('Personal_Cell_No', employee.Personal_Cell_No)
        employee.Official_Cell_No = emp_data.get('Official_Cell_No', employee.Official_Cell_No)
        employee.Email = emp_data.get('Email', employee.Email)
        employee.TEL_EXT = emp_data.get('TEL_EXT', employee.TEL_EXT)
        employee.Gender = emp_data.get('Gender', employee.Gender)
        employee.Marital_Status = emp_data.get('Marital_Status', employee.Marital_Status)
        employee.CNIC_No = emp_data.get('CNIC_No', employee.CNIC_No)
        employee.Religion = emp_data.get('Religion', employee.Religion)
        employee.Co_ID = emp_data.get('Co_ID', employee.Co_ID)

        # Handle foreign keys
        ct_id = emp_data.get('CT_ID')
        if ct_id:
            employee.CT_ID = HR_City.objects.get(pk=ct_id)

        joining_dsg_id = emp_data.get('Joining_Dsg_ID')
        if joining_dsg_id:
            employee.Joining_Dsg_ID = HR_Designation.objects.get(pk=joining_dsg_id)

        joining_dept_id = emp_data.get('Joining_Dept_ID')
        if joining_dept_id:
            employee.Joining_Dept_ID = HR_Department.objects.get(pk=joining_dept_id)

        # Handle date fields
        confirmation_date = emp_data.get('Confirmation_Date')
        if confirmation_date:
            employee.Confirmation_Date = timezone.datetime.strptime(confirmation_date, "%Y-%m-%d").date()

        cnic_issue_date = emp_data.get('CNIC_Issue_Date')
        if cnic_issue_date:
            employee.CNIC_Issue_Date = timezone.datetime.strptime(cnic_issue_date, "%Y-%m-%d").date()

        cnic_exp_date = emp_data.get('CNIC_Exp_Date')
        if cnic_exp_date:
            employee.CNIC_Exp_Date = timezone.datetime.strptime(cnic_exp_date, "%Y-%m-%d").date()

        date_of_birth = emp_data.get('DateOfBirth')
        if date_of_birth:
            employee.DateOfBirth = timezone.datetime.strptime(date_of_birth, "%Y-%m-%d").date()

        # Handle profile image
        if 'ProfileImage' in request.FILES:
            profile_image = request.FILES['ProfileImage']
            ext = profile_image.name.split('.')[-1]  # Get the file extension
            profile_image_name = f"{employee.HR_Emp_ID}.{ext}"  # Construct the new filename

            # Delete old profile image if it exists
            if employee.ProfileImage and default_storage.exists(employee.ProfileImage.name):
                default_storage.delete(employee.ProfileImage.name)

            # Save new profile image with the hr_empid name
            employee.ProfileImage.save(profile_image_name, profile_image, save=False)

        employee.save()

        emp_serializer = HR_Employees_Serializer(employee)
        return Response(emp_serializer.data, status=200)

    except Exception as e:
        return Response({'message': str(e)}, status=500)

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
    
class GroupOfCompaniesListView(generics.ListCreateAPIView):
    queryset = GroupOfCompanies.objects.all()
    serializer_class = GroupOfCompaniesSerializer

