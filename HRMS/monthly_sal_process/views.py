from django.shortcuts import render
from rest_framework.generics import ListAPIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import HR_Emp_Monthly_Sal_Mstr, HR_Emp_Monthly_Sal_Dtl
from .serializer import HR_Emp_Monthly_Sal_Dtl_Serializer, HR_Emp_Monthly_Sal_Mstr_Serializer
from employee.models import HR_Employees
from employee.serializers import HR_Employees_Serializer
from django.db.models import Subquery
from rest_framework import status
from payroll_element.models import HR_Payroll_Elements, HR_Payroll_Elements_Serializer
import pdb
from payroll_period.models import *
from salary_update.models import HR_Emp_Sal_Update_Mstr, HR_Emp_Sal_Update_Dtl
from salary_update.serializer import *
from django.db.models import Max
from django.db import models, transaction
from django.db.models import F, Value, FloatField
from django.db.models.functions import Cast
from django.utils import timezone
from django.db import connection
from django.http import JsonResponse
from grade.models import HR_Grade
from designation.models import HR_Designation
from department.models import HR_Department
from django.db.models import Sum, F, Value
from django.db import transaction
from django.db.models import Sum, F, Value, Case, When
from django.db.models.functions import Coalesce
from django.db import transaction
from django.http import HttpResponse
import requests
from django.db.models import Q
from celery import shared_task
from django.db import connection, transaction

def salaryprocess_view(request):
    return render(request, 'salaryprocess.html')

def monthlysalaryupdate_view(request):
    return render(request, 'monthlysalaryupdate.html')

# this is currently working now
def execute_salary_process2(request, payroll_id, fuel_rate):
    print('execute_salary_process2 called')
    import pdb
    pdb.set_trace()
    payroll_period = HR_PAYROLL_PERIOD.objects.filter(PAYROLL_ID=payroll_id).first()
    if payroll_period.PAYROLL_FINAL:
        return JsonResponse({
            'ResponseCode': 201,
            'Message': 'Payroll Process Already Executed',
            'Data': None
        })

    api_url = 'http://localhost:5000/ExecuteSalaryProcess/'
    payload = {
        'm_Payroll_ID': payroll_id,
        'm_Fuel_Rate': fuel_rate
    }

    try:
        headers = {'Content-Type': 'application/json'}
        response = requests.post(api_url, json=payload, headers=headers, verify=False)

        print(f'Response Status Code: {response.status_code}')
        print(f'Response Content: {response.content.decode()}')

        # If the response status code is 200 OK
        if response.status_code == 200:
            response_data = response.json()
            return JsonResponse({
                'ResponseCode': response_data.get('ResponseCode', 500),
                'Message': response_data.get('Message', 'Failed to execute'),
                'Data': response_data.get('Data', None)
            })
        else:
            return JsonResponse({
                'ResponseCode': response.status_code,
                'Message': 'Failed to execute external API',
                'Data': None
            })
    except requests.RequestException as e:
        return JsonResponse({
            'ResponseCode': 500,
            'Message': f'Error occurred: {str(e)}',
            'Data': None
        })

def execute_salary_process(request, payroll_id, fuel_rate):
    import pdb
    pdb.set_trace()
    print('execute_salary_process')
    api_url = 'https://localhost:44339/api/SalaryUpdate/ExecuteSalaryProcess'
    params = {
        'Payroll_ID': payroll_id, 
        'Fuel_ID': fuel_rate
    }
    headers = {
        'Authorization': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJVc2VyX0lEIjoiMiIsIm5iZiI6MTcyMjYyMjMzMiwiZXhwIjoxNzIzMjI3MTMyLCJpYXQiOjE3MjI2MjIzMzJ9._yFPxWiBp8EZJk5YBdj3VIKXjuNXLk_JAwbtKxBiFLA'
    }

    try:

        # payroll_period = HR_PAYROLL_PERIOD.objects.filter(PAYROLL_ID=payroll_id).select_related('MNTH_ID', 'FYID').first()
        
        # if not payroll_period:
        #     return JsonResponse({
        #         'ResponseCode': 404,
        #         'Message': 'Payroll period not found',
        #         'Data': None
        #     })
        
        # print('PAYROLL_FINAL: ', payroll_period.PAYROLL_FINAL)

        # if not payroll_period.PAYROLL_FINAL:
        #     return JsonResponse({
        #         'ResponseCode': 500,
        #         'Message': 'Payroll is not finalized',
        #         'Data': None
        #     })

        response = requests.get(api_url, params=params, headers=headers, verify=False)  

        if response.status_code == 200:
            response_data = response.json()
            return JsonResponse({
                'ResponseCode': response_data.get('ResponseCode', 500),
                'Message': response_data.get('Message', 'Failed to execute'),
                'Data': response_data.get('Data', None)
            })
        else:
            return JsonResponse({
                'ResponseCode': response.status_code,
                'Message': 'Failed to execute external API',
                'Data': None
            })
    except requests.RequestException as e:
        return JsonResponse({
            'ResponseCode': 500,
            'Message': f'Error occurred: {str(e)}',
            'Data': None
        })

def hr_monthly_salary_process(request, payroll_id, fuel_rate):
    try:
        payroll_period = HR_PAYROLL_PERIOD.objects.get(PAYROLL_ID=payroll_id)
    except HR_PAYROLL_PERIOD.DoesNotExist:
        return HttpResponse("Payroll period does not exist", status=404)

    # Delete existing data in destination tables
    HR_Emp_Monthly_Sal_Mstr.objects.filter(Payroll_ID=payroll_period).delete()
    HR_Emp_Monthly_Sal_Dtl.objects.filter(Payroll_ID=payroll_period).delete()

    # Fetch data for bulk create
    salary_updates = HR_Emp_Sal_Update_Mstr.objects.filter(Emp_ID__Emp_Status=1, Stop_Salary=0).select_related('Emp_ID', 'Dsg_ID', 'Dept_ID', 'Grade_ID')
    salary_details = HR_Emp_Sal_Update_Dtl.objects.filter(Emp_ID__Emp_Status=1, Emp_ID__in=salary_updates.values('Emp_ID')).select_related('Emp_Up_ID', 'Element_ID', 'Emp_ID')

    # Insert into HR_Emp_Monthly_Sal_Mstr
    salary_masters = [
        HR_Emp_Monthly_Sal_Mstr(
            Payroll_ID=payroll_period,
            Emp_Up_ID=obj.Emp_Up_ID,
            Emp_Up_Date=obj.Emp_Up_Date,
            Emp_ID=obj.Emp_ID,
            Emp_Category=obj.Emp_Category,
            HR_Emp_ID=obj.HR_Emp_ID,
            Marital_Status=obj.Marital_Status,
            No_of_Children=obj.No_of_Children,
            Dsg_ID=obj.Dsg_ID,
            Dept_ID=obj.Dept_ID,
            Grade_ID=obj.Grade_ID,
            Co_ID=obj.Co_ID,
            Remarks=obj.Remarks,
            GrossSalary=obj.GrossSalary,
            MDays=30,
            WDAYS=0,
            ADAYS=0,
            JLDAYS=0,
            Transfer_Type=obj.Transfer_Type,
            Account_No=obj.Account_No,
            Bank_Name=obj.Bank_Name,
            Stop_Salary=obj.Stop_Salary
        )
        for obj in salary_updates
    ]
    HR_Emp_Monthly_Sal_Mstr.objects.bulk_create(salary_masters)

    # Insert into HR_Emp_Monthly_Sal_Dtl
    salary_details_bulk = [
        HR_Emp_Monthly_Sal_Dtl(
            Payroll_ID=payroll_period,
            Emp_Up_ID=obj.Emp_Up_ID.Emp_Up_ID,
            Emp_ID=obj.Emp_ID,
            Element_ID=obj.Element_ID,
            Amount=obj.Amount,
            Element_Type=obj.Element_Type,
            Element_Category=obj.Element_Category
        )
        for obj in salary_details
    ]
    HR_Emp_Monthly_Sal_Dtl.objects.bulk_create(salary_details_bulk)

    # Update Fixed Additional Elements
    for detail in HR_Emp_Monthly_Sal_Dtl.objects.filter(Element_Category='Fixed Additional'):
        emp = HR_Employees.objects.get(Emp_ID=detail.Emp_ID.Emp_ID)
        joining_date = emp.Joining_Date
        last_working_date = emp.Last_Working_Date

        if joining_date and last_working_date:
            total_days = (last_working_date - joining_date).days
            if total_days > 0:
                working_days = (30 - (joining_date - payroll_period.Payroll_Start_Date).days) # Assuming `Payroll_Start_Date` is the start date of the payroll period
                new_amount = (detail.Amount / total_days) * working_days
            else:
                new_amount = 0

            detail.Amount = new_amount
            detail.save()

    return JsonResponse({'results': "Procedure executed successfully!"})

@api_view(['GET'])
def transfer_data_to_salary_process(request, payroll_id, fuel_rate):
    print('transfer_data_to_salary_process called payroll_id: ', payroll_id)
    try:
        with connection.cursor() as cursor:
            # Example with output parameter
            output_param = cursor.callproc('dbo.HR_Monthly_Salary_Process', [payroll_id, fuel_rate])
            
            # Example to fetch output parameter value
            result = output_param[2]  # Adjust index based on your output parameter
            
            rows_affected = cursor.rowcount
            print(f"Rows affected: {rows_affected}, Output: {result}")

        return JsonResponse({'results': f"Procedure executed successfully. Rows affected: {rows_affected}, Output: {result}"})
    except Exception as e:
        print(f"Error executing stored procedure: {str(e)}")
        return JsonResponse({'error': f"Error executing stored procedure: {str(e)}"}, status=500)

@api_view(['GET'])
def transfer_data_to_salary_process2(request, payroll_id, fuel_rate):
    print('transfer_data_to_salary_process called payroll_id: ', payroll_id)
    try:
        with connection.cursor() as cursor:
            cursor.execute("EXEC dbo.HR_Monthly_Salary_Process @m_Payroll_ID=%s, @m_Fuel_Rate=%s", [payroll_id, fuel_rate])
            
            rows_affected = cursor.rowcount
            print(f"Rows affected: {rows_affected}")

            # results = cursor.fetchall()

        return JsonResponse({'results': f"Procedure executed successfully. Rows affected: {rows_affected}"})
    except Exception as e:
        print(f"Error executing stored procedure: {str(e)}")

# celery functions
# this is working we are calling SP from Django now
@shared_task
def run_monthly_salary_process_celery(request, payroll_id, fuel_rate):
    try:
        with connection.cursor() as cursor:
            # Enable autocommit for this execution
            with transaction.atomic():
                cursor.execute(
                    "SET NOCOUNT ON; EXEC HR_Monthly_Salary_Process @m_Payroll_ID=%s, @m_Fuel_Rate=%s",
                    [payroll_id, fuel_rate]
                )

            try:
                # Consume all result sets
                while True:
                    try:
                        results = cursor.fetchall()
                        columns = [col[0] for col in cursor.description]
                        data = [dict(zip(columns, row)) for row in results]
                    except Exception:
                        data = []

                    if not cursor.nextset():
                        break

            except Exception:
                data = []

        return JsonResponse({
            "ResponseCode": 200 if data else 204,
            "Message": "Salary process executed successfully" if data else "No data returned",
            "Data": data
        })

    except Exception as e:
        return JsonResponse({
            "ResponseCode": 500,
            "Message": f"Error while executing Salary Process: {str(e)}",
            "Data": None
        })

@api_view(['GET'])
def get_salarystatus_distinct(request):
    try:
        # Fetch distinct Salary_Status values
        distinct_salarystatus = HR_Emp_Monthly_Sal_Mstr.objects.values('Salary_Status').distinct()
        # Convert queryset to a list of distinct values
        result = [entry['Salary_Status'] for entry in distinct_salarystatus if entry['Salary_Status'] is not None]
        return Response(data=result, status=200)
    except Exception as e:
        return Response({'error': str(e)}, status=500)

        
@api_view(['GET'])
def getall_payrollperiod(request):
    try:
        payroll_periods = HR_PAYROLL_PERIOD.objects.select_related('MNTH_ID', 'FYID').all()

        data = []

        for payroll_period in payroll_periods:
            data.append({
                'PAYROLL_ID': payroll_period.PAYROLL_ID,
                'PERIOD_ID': payroll_period.PERIOD_ID,
                'MNTH_NAME': payroll_period.MNTH_ID.MNTH_NAME,
                'FinYear': payroll_period.FYID.FinYear
            })

        return Response(data=data, status=200)

    except Exception as e:
        return Response({'error': str(e)}, status=500)

@api_view(['GET'])
def get_active_period_old(request):
    try:
        payroll_period = HR_PAYROLL_PERIOD.objects.filter(PERIOD_STATUS=True, FYID__FYID=1).select_related('MNTH_ID', 'FYID').first()

        payroll_period.FYID.FinYear

        # if payroll_period:
        data = {
            'PAYROLL_ID': payroll_period.PAYROLL_ID,
            'PERIOD_ID': payroll_period.PERIOD_ID,
            'MNTH_NAME': payroll_period.MNTH_ID.MNTH_NAME,
            'FinYear': payroll_period.FYID.FinYear
        }

        print('get_active_period: ', data)

        return Response(data=data, status=200)
    except Exception as e:
        return Response({'error': str(e)}, status=500)


@api_view(['GET'])
def get_active_period(request):
    with connection.cursor() as cursor:
        # Run the raw SQL query
        cursor.execute("SELECT Payroll_ID, FYID, MNTH_SHORT_NAME, PERIOD_STATUS, Yr FROM HR_PAYROLL_PERIOD_V WHERE PERIOD_STATUS = 1")
        
        # Fetch all results
        rows = cursor.fetchall()
        
        # Get column names
        columns = [col[0] for col in cursor.description]
        
        # Convert query results to list of dictionaries
        result = [dict(zip(columns, row)) for row in rows]

        print('active period: ', result)

    # Return the result as JSON
    return JsonResponse(result, safe=False)


@api_view(['GET'])  
def getall_salaryprocess(request):
    try:
        emp_ids = HR_Emp_Monthly_Sal_Mstr.objects.values('Emp_ID')
        queryset_emp_salaryprocess = HR_Employees.objects.exclude(Emp_ID__in=Subquery(emp_ids)).all()    
        serializer = HR_Employees_Serializer(queryset_emp_salaryprocess, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])  
def getll_emp_notin_salaryprocess(request):
    try:
        emp_ids = HR_Emp_Monthly_Sal_Mstr.objects.values('Emp_ID')
        queryset_emp_salaryprocess = HR_Employees.objects.exclude(Emp_ID__in=Subquery(emp_ids)).all()
        serializer = HR_Employees_Serializer(queryset_emp_salaryprocess, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def add_salary_update(request):
        try:
            # print("add_salary_update data: ", request.data)   
            # pdb.set_trace()
            print("add_salary_update")
            print("masterData data: ", request.data.get("masterData", {}))
            print("detailList data: ", request.data.get('detailList', []))
            master_serializer = HR_Emp_Monthly_Sal_Mstr_Serializer(data=request.data.get("masterData", {}))
            if master_serializer.is_valid():
                master_serializer.save()
                print("master saved")
                print("master_serializer: ", master_serializer.data)
                print("master_serializer.data.Emp_Up_ID: ", master_serializer.data['Emp_Up_ID'])
                detailList = request.data.get('detailList', [])
                for detail_data in detailList:
                    detail_data['Emp_Up_ID'] = master_serializer.data['Emp_Up_ID']
                    detail_data['Emp_ID'] = master_serializer.data['Emp_ID']
                    detail_serializer = HR_Emp_Monthly_Sal_Dtl_Serializer(data=detail_data)
                    if detail_serializer.is_valid():
                        detail_serializer.save()
                        print("detail saved")
                    else:
                        return Response(detail_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                return Response(master_serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(master_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# @api_view(['POST'])
# def update_salary_update(request, empupid):
#         try:
#             print("update_salary_update")
#             print("empupid: ", empupid)
#             print("masterData data: ", request.data.get("masterData", {}))
#             print("detailList data: ", request.data.get('detailList', []))
#             master_querysery = HR_Emp_Monthly_Sal_Mstr.objects.get(pk=empupid)
#             detail_queryset = HR_Emp_Monthly_Sal_Mstr.objects.get(Emp_Up_ID=empupid)
#             if master_querysery is None:
#                 Response({'error': 'no salary found'}, status=status.HTTP_404_NOT_FOUND)
            
#             # if master_querysery and detail_queryset is not None:
#             #     HR_Emp_Monthly_Sal_Mstr.objects.filter(Emp_Up_ID=empupid).delete()
#             #     HR_Emp_Monthly_Sal_Dtl.objects.filter(Emp_Up_ID=empupid).delete()

#             master_serializer = HR_Emp_Monthly_Sal_Mstr_Serializer(data=request.data.get("masterData", {}))
#             # master_serializer = HR_Emp_Monthly_Sal_Mstr_Serializer(master_querysery, data=request.data.get("masterData", {}), partial=True)
#             if master_serializer.is_valid():
#                 master_serializer.save()
#                 print("master updated")
#                 print("master_serializer: ", master_serializer.data)
#                 print("master_serializer.data.Emp_Up_ID: ", master_serializer.data['Emp_Up_ID'])
#                 detailList = request.data.get('detailList', [])

#                 for detail_data in detailList:
#                     detail_data['Emp_Up_ID'] = master_serializer.data['Emp_Up_ID']
#                     detail_data['Emp_ID'] = master_serializer.data['Emp_ID']
        
#                     # detail_queryset = HR_Emp_Monthly_Sal_Dtl.objects.get(Emp_ID=empupid)

#                     detail_serializer = HR_Emp_Monthly_Sal_Dtl_Serializer(data=detail_data)
#                     if detail_serializer.is_valid():
#                         detail_serializer.save()
#                         print("detail updated")
#                     else:
#                         return Response(detail_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#             return Response(master_serializer.data, status=status.HTTP_200_OK)
#         except Exception as e:
#             return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# @api_view(['POST'])
# def update_salary_update(request, empupid):
#         try:
#             print("monthly update salary")
#             print("empupid: ", empupid)
#             print("masterData data: ", request.data.get("masterData", {}))
#             print("detailList data: ", request.data.get('detailList', []))
#             master_querysery = HR_Emp_Monthly_Sal_Mstr.objects.get(pk=empupid)
#             detail_queryset =  HR_Emp_Monthly_Sal_Dtl.objects.filter(Emp_Up_ID=empupid)
#             print('detail_queryset: ', detail_queryset.__dict__)
#             if master_querysery is None:
#                 Response({'error': 'no salary found'}, status=status.HTTP_404_NOT_FOUND)
            
#             if master_querysery and detail_queryset is not None:
#                 HR_Emp_Monthly_Sal_Mstr.objects.filter(Emp_Up_ID=empupid).delete()
#                 HR_Emp_Monthly_Sal_Dtl.objects.filter(Emp_Up_ID=empupid).delete()

#             master_serializer = HR_Emp_Monthly_Sal_Mstr_Serializer(data=request.data.get("masterData", {}))
#             # master_serializer = HR_Emp_Sal_Update_Mstr_Serializer(master_querysery, data=request.data.get("masterData", {}), partial=True)
           
#             print('called update: ', master_serializer)
#             print('called update valid()')
#             if master_serializer.is_valid():
#                 print('called update valid() passed!')
#                 master_serializer.save()
#                 print("master updated")
#                 print("master_serializer: ", master_serializer.data)
#                 print("master_serializer.data.Emp_Up_ID: ", master_serializer.data['Emp_Up_ID'])
#                 detailList = request.data.get('detailList', [])

#                 for detail_data in detailList:
#                     detail_data['Emp_Up_ID'] = master_serializer.data['Emp_Up_ID']
#                     detail_data['Emp_ID'] = master_serializer.data['Emp_ID']
#                     detail_data['Payroll_ID'] = master_serializer.data['Payroll_ID'] 
        
#                     # detail_queryset = HR_Emp_Sal_Update_Dtl.objects.get(Emp_ID=empupid)

#                     detail_serializer = HR_Emp_Monthly_Sal_Dtl_Serializer(data=detail_data)
#                     if detail_serializer.is_valid():
#                         detail_serializer.save()
#                         print("detail updated")
#                     else:
#                         return Response(detail_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#             else:
#                 return Response(master_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#             return Response(master_serializer.data, status=status.HTTP_200_OK)
#         except Exception as e:
#             return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



# @api_view(['POST'])
# def update_salary_update_new_one(request, empupid, payroll_id):
#     try:
#         # Fetch master data
#         master_instance = HR_Emp_Monthly_Sal_Mstr.objects.filter(Emp_Up_ID=empupid, Payroll_ID__PAYROLL_ID=payroll_id).first()
#         if not master_instance:
#             return Response({'error': 'No salary record found'}, status=status.HTTP_404_NOT_FOUND)

#         print('master_instance: ', master_instance.__dict__)

#         # Handle master data update
#         master_serializer = HR_Emp_Monthly_Sal_Mstr_Serializer(master_instance, data=request.data.get("masterData", {}), partial=True)
#         if master_serializer.is_valid():
#             master_instance = master_serializer.save()

#             # Retrieve detail data list from the request
#             detailList = request.data.get('detailList', [])
#             for detail_data in detailList:
#                 # Prepare the data to be saved
#                 detail_data['Emp_Up_ID'] = master_instance.Emp_Up_ID
#                 detail_data['Emp_ID'] = master_instance.Emp_ID.Emp_ID
#                 detail_data['Payroll_ID'] = master_instance.Payroll_ID.PAYROLL_ID

#                 # Check if a matching record already exists
#                 detail_instance = HR_Emp_Monthly_Sal_Dtl.objects.filter(
#                     Emp_Up_ID=master_instance.Emp_Up_ID,
#                     Emp_ID=master_instance.Emp_ID.Emp_ID,
#                     Payroll_ID=master_instance.Payroll_ID.PAYROLL_ID,
#                     Element_ID=detail_data.get('Element_ID')  # Assuming 'Element_ID' uniquely identifies the record
#                 ).first()

#                 if detail_instance:
#                     # Update existing record
#                     detail_serializer = HR_Emp_Monthly_Sal_Dtl_Serializer(detail_instance, data=detail_data, partial=True)
#                 else:
#                     # Create a new record if none exists
#                     detail_serializer = HR_Emp_Monthly_Sal_Dtl_Serializer(data=detail_data)

#                 # Validate and save each detail record
#                 if detail_serializer.is_valid():
#                     detail_serializer.save()
#                     print(f"Detail record saved for Element_ID: {detail_data.get('Element_ID')}")
#                 else:
#                     return Response(detail_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#             return Response(master_serializer.data, status=status.HTTP_200_OK)
#         else:
#             return Response(master_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#     except HR_Emp_Monthly_Sal_Mstr.MultipleObjectsReturned:
#         return Response({'error': 'Multiple salary records found. Please refine your query.'}, status=status.HTTP_400_BAD_REQUEST)
#     except Exception as e:
#         return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def update_salary_update(request, empupid, payroll_id):
    """
    Updates salary master and detail records for a given employee and payroll.
    """
    try:
        # Fetch master instance
        master_instance = HR_Emp_Monthly_Sal_Mstr.objects.filter(
            Emp_Up_ID=empupid, 
            Payroll_ID__PAYROLL_ID=payroll_id
        ).first()
        
        if not master_instance:
            return Response({'error': 'No salary record found'}, status=status.HTTP_404_NOT_FOUND)
        
        # Log fetched master instance
        print('Master instance fetched:', master_instance)

        # Validate and update master data
        master_data = request.data.get("masterData", {})
        master_serializer = HR_Emp_Monthly_Sal_Mstr_Serializer(
            master_instance, 
            data=master_data, 
            partial=True
        )

        if not master_serializer.is_valid():
            return Response(master_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Save changes to master instance
        with transaction.atomic():
            master_instance = master_serializer.save()

        print('Master data updated successfully.')

        # Process detail data
        detail_list = request.data.get('detailList', [])
        for detail_data in detail_list:
            detail_data.update({
                'Emp_Up_ID': master_data.get("Emp_Up_ID"),
                'Emp_ID': master_data.get("Emp_ID"),
                'Payroll_ID': master_data.get("Payroll_ID")
            })

            # Check if detail record exists
            detail_instance = HR_Emp_Monthly_Sal_Dtl.objects.filter(
                Emp_Up_ID=master_data.get("Emp_Up_ID"),
                Emp_ID=master_data.get("Emp_ID"),
                Payroll_ID=master_data.get("Payroll_ID"),
                Element_ID=detail_data.get('Element_ID')
            ).first()

            # Choose serializer for update or create
            detail_serializer = HR_Emp_Monthly_Sal_Dtl_Serializer(
                detail_instance, 
                data=detail_data, 
                partial=bool(detail_instance)
            )

            if not detail_serializer.is_valid():
                return Response(detail_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            # Save detail record
            with transaction.atomic():
                detail_serializer.save()

            print(f"Detail record processed for Element_ID: {detail_data.get('Element_ID')}")

        # Return success response
        return Response(master_serializer.data, status=status.HTTP_200_OK)

    except Exception as e:
        print(f"Error occurred: {e}")
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# @api_view(['PUT'])
# def update_salary_Update(request, pk):
#     try:
#         master_instance = HR_Emp_Monthly_Sal_Mstr.objects.get(pk=pk)
#         master_serializer = HR_Emp_Monthly_Sal_Mstr_Serializer(instance=master_instance, data=request.data.get('masterData', {}))
#         if not master_serializer.is_valid():
#             return Response(master_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#         master_serializer.save()

#         detail_querySet_list = HR_Emp_Monthly_Sal_Dtl.objects.filter(Emp_Up_ID=pk)
#         for detail_querySet in detail_querySet_list:
#             detail_request = next((item for item in request.data.get("detailList", []) if item['id'] == detail_querySet.id), None)
#             if detail_request:
#                 detail_serializer = HR_Emp_Monthly_Sal_Dtl_Serializer(instance=detail_querySet, data=detail_request)
#                 if detail_serializer.is_valid():
#                     detail_serializer.save()
#                 else:
#                     return Response(detail_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#         return Response({"message": "Salary update updated successfully"}, status=status.HTTP_200_OK)
#     except HR_Emp_Monthly_Sal_Mstr.DoesNotExist:
#         return Response({'error': 'Master record not found'}, status=status.HTTP_404_NOT_FOUND)
#     except Exception as e:
#         return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def getall_payroll_element_notin_su(request, empUpID, empID):
    try:
        print('empID: ', empID)
        print('empUpID: ', empUpID)
        if empID is None or empUpID is None:
            return Response({'error': 'Salary not found'}, status=status.HTTP_404_NOT_FOUND)
        su_queryset = HR_Emp_Monthly_Sal_Dtl.objects.filter(Emp_ID=empID, Emp_Up_ID=empUpID).values_list("Element_ID", flat=True)
        element_queryset = HR_Payroll_Elements.objects.filter(Q(Element_Category='Fixed Additional') | Q(Element_Category='Additional')).exclude(Element_ID__in=su_queryset)
        serializer = HR_Payroll_Elements_Serializer(element_queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['GET'])
def getall_master_byid(request, empUpID, empID, payroll_id):
    try:
        if not empID or not empUpID:
            return Response({'error': 'Employee ID or Update ID not provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Fetching data
        detail_queryset = HR_Emp_Monthly_Sal_Dtl.objects.filter(
            Emp_Up_ID__Emp_Up_ID=empUpID,
            Emp_ID__Emp_ID=empID,
            Payroll_ID__PAYROLL_ID=payroll_id
        ).select_related('Emp_Up_ID', 'Emp_ID', 'Element_ID')

        print('detail_queryset count: ', detail_queryset.count())

        # Use a set to track unique keys (e.g., Emp_Up_ID + Emp_ID)
        unique_data = {}
        
        # Loop through the queryset
        for data in detail_queryset:
            # Create a unique key for each employee
            unique_key = (data.Emp_Up_ID.Emp_Up_ID, data.Emp_ID.Emp_ID, data.Element_ID.Element_ID)

            # Check if this unique combination already exists
            if unique_key not in unique_data:
                # If not, add it to the unique_data dictionary
                unique_data[unique_key] = {
                    "Emp_Up_ID": data.Emp_Up_ID.Emp_Up_ID,
                    "Emp_Up_Date": data.Emp_Up_ID.Emp_Up_Date,
                    "Emp_ID": data.Emp_ID.Emp_ID,
                    "Emp_Name": data.Emp_ID.Emp_Name,
                    "HR_Emp_ID": data.Emp_ID.HR_Emp_ID,
                    "Emp_Category": data.Emp_Up_ID.Emp_Category,
                    "GrossSalary": data.Emp_Up_ID.GrossSalary,  
                    "Amount": data.Amount,
                    "Element_Category": data.Element_Category,
                    "Element_ID": data.Element_ID.Element_ID,
                    "Element_Name": data.Element_ID.Element_Name,
                    "Element_Type": data.Element_Type,
                    "Remarks": data.Emp_Up_ID.Remarks,
                    "Grade_ID": data.Emp_Up_ID.Grade_ID.Grade_ID,
                    "Grade_Descr": data.Emp_Up_ID.Grade_ID.Grade_Descr,
                    "Co_ID": data.Emp_ID.Co_ID,
                    "Dsg_ID": data.Emp_Up_ID.Dsg_ID.DSG_ID,
                    "DSG_Descr": data.Emp_Up_ID.Dept_ID.Dept_Descr,
                    "Dept_ID": data.Emp_Up_ID.Dept_ID.Dept_ID,
                    "Dept_Descr": data.Emp_Up_ID.Dept_ID.Dept_Descr,
                    "Marital_Status": data.Emp_ID.Marital_Status,
                    "No_of_Children": data.Emp_Up_ID.No_of_Children,
                    "Transfer_Type": data.Emp_Up_ID.Transfer_Type,
                    "Account_No": data.Emp_Up_ID.Account_No,
                    "Bank_Name": data.Emp_Up_ID.Bank_Name,
                    "Stop_Salary": data.Emp_Up_ID.Stop_Salary,
                    'Payroll_ID': data.Payroll_ID.PAYROLL_ID,
                    'Salary_Status': data.Emp_Up_ID.Salary_Status,
                    'Payroll_Name': f'{data.Payroll_ID.MNTH_ID.MNTH_NAME} {data.Payroll_ID.FYID.FinYear}',
                }
        
        # Now convert the dictionary values to a list
        datas = list(unique_data.values())

        print("Final data count: ", len(datas))
        return Response(datas, status=status.HTTP_200_OK)

    except HR_Emp_Monthly_Sal_Dtl.DoesNotExist:
        return Response({'error': 'Salary not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



# @api_view(['GET'])
# def getall_master_byid(request, empUpID, empID, payroll_id):
#     try:
#         if not empID or not empUpID:
#             return Response({'error': 'Employee ID or Update ID not provided'}, status=status.HTTP_400_BAD_REQUEST)
        
#         # Fetching data with distinct records
#         detail_queryset = HR_Emp_Monthly_Sal_Dtl.objects.filter(
#             Emp_Up_ID__Emp_Up_ID=empUpID,
#             Emp_ID__Emp_ID=empID,
#             Payroll_ID__PAYROLL_ID=payroll_id
#         ).select_related('Emp_Up_ID', 'Emp_ID', 'Element_ID').distinct()

#         datas = []

#         print('detail_queryset: ', detail_queryset)

#         print('detail_queryset count: ', detail_queryset.count())

#         counter = 0
#         # Appending unique data to list
#         for data in detail_queryset:
#             counter += 1
#             print('data: data: ', data)
#             # print('counter: ', counter)
#             print(f"Loop iteration {counter}: Data Element_ID {data.Element_ID.Element_ID}")  # Print which record is processed

#             item = {
#                 "Emp_Up_ID": data.Emp_Up_ID.Emp_Up_ID,
#                 "Emp_Up_Date": data.Emp_Up_ID.Emp_Up_Date,
#                 "Emp_ID": data.Emp_ID.Emp_ID,
#                 "Emp_Name": data.Emp_ID.Emp_Name,
#                 "HR_Emp_ID": data.Emp_ID.HR_Emp_ID,
#                 "Emp_Category": data.Emp_Up_ID.Emp_Category,
#                 "GrossSalary": data.Emp_Up_ID.GrossSalary,  
#                 "Amount": data.Amount,
#                 "Element_Category": data.Element_Category,
#                 "Element_ID": data.Element_ID.Element_ID,
#                 "Element_Name": data.Element_ID.Element_Name,
#                 "Element_Type": data.Element_Type,
#                 "Remarks": data.Emp_Up_ID.Remarks,
#                 "Grade_ID": data.Emp_Up_ID.Grade_ID.Grade_ID,
#                 "Grade_Descr": data.Emp_Up_ID.Grade_ID.Grade_Descr,
#                 "Co_ID": data.Emp_ID.Co_ID,
#                 "Dsg_ID": data.Emp_Up_ID.Dsg_ID.DSG_ID,
#                 "DSG_Descr": data.Emp_Up_ID.Dept_ID.Dept_Descr,
#                 "Dept_ID": data.Emp_Up_ID.Dept_ID.Dept_ID,
#                 "Dept_Descr": data.Emp_Up_ID.Dept_ID.Dept_Descr,
#                 "Marital_Status": data.Emp_ID.Marital_Status,
#                 "No_of_Children": data.Emp_Up_ID.No_of_Children,
#                 "Transfer_Type": data.Emp_Up_ID.Transfer_Type,
#                 "Account_No": data.Emp_Up_ID.Account_No,
#                 "Bank_Name": data.Emp_Up_ID.Bank_Name,
#                 "Stop_Salary": data.Emp_Up_ID.Stop_Salary,
#                 'Payroll_ID': data.Payroll_ID.PAYROLL_ID,
#                 'Payroll_Name': f'{data.Payroll_ID.MNTH_ID.MNTH_NAME} {data.Payroll_ID.FYID.FinYear}',
#             }
#             datas.append(item)
        
#         print("Datas count: ", len(datas))
#         return Response(datas, status=status.HTTP_200_OK)

#     except HR_Emp_Monthly_Sal_Dtl.DoesNotExist:
#         return Response({'error': 'Salary not found'}, status=status.HTTP_404_NOT_FOUND)
#     except Exception as e:
#         return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



# @api_view(['GET'])
# def getall_master_byid(request, empUpID, empID, payroll_id):
#     try:
#         if not empID or not empUpID:
#             return Response({'error': 'Employee ID or Update ID not provided'}, status=status.HTTP_400_BAD_REQUEST)
#         print("up is: ", empUpID)
#         print("empID: ", empID)
#         print("payroll_id: ", payroll_id)
#         # detail_queryset = HR_Emp_Monthly_Sal_Dtl.objects.filter(Emp_Up_ID=empUpID)
#         detail_queryset = HR_Emp_Monthly_Sal_Dtl.objects.filter(Emp_Up_ID__Emp_Up_ID=empUpID, Emp_ID__Emp_ID=empID, Payroll_ID__PAYROLL_ID=payroll_id).select_related('Emp_Up_ID', 'Emp_ID', 'Element_ID')
#         # detail_queryset = HR_Emp_Monthly_Sal_Dtl.objects.filter(Emp_Up_ID=empUpID, Emp_ID=empID)
#         datas = []
#         print('detail_queryset: ', detail_queryset)
#         print('detail_queryset count: ', detail_queryset.count())
#         for data in detail_queryset:
#             # print('data: ', data)
#             item = {
#                 "Emp_Up_ID": data.Emp_Up_ID.Emp_Up_ID,
#                 "Emp_Up_Date": data.Emp_Up_ID.Emp_Up_Date,
#                 "Emp_ID": data.Emp_ID.Emp_ID,
#                 "Emp_Name": data.Emp_ID.Emp_Name,
#                 "HR_Emp_ID": data.Emp_ID.HR_Emp_ID,
#                 "Emp_Category": data.Emp_Up_ID.Emp_Category,
#                 "GrossSalary": data.Emp_Up_ID.GrossSalary,  
#                 "Amount": data.Amount,
#                 "Element_Category": data.Element_Category,
#                 "Element_ID": data.Element_ID.Element_ID,
#                 "Element_Name": data.Element_ID.Element_Name,
#                 "Element_Type": data.Element_Type,
#                 "Remarks": data.Emp_Up_ID.Remarks,
#                 "Grade_ID": data.Emp_Up_ID.Grade_ID.Grade_ID,
#                 "Grade_Descr": data.Emp_Up_ID.Grade_ID.Grade_Descr,
#                 "Co_ID": data.Emp_ID.Co_ID,
#                 "Dsg_ID": data.Emp_Up_ID.Dsg_ID.DSG_ID,
#                 "DSG_Descr": data.Emp_Up_ID.Dept_ID.Dept_Descr,
#                 "Dept_ID": data.Emp_Up_ID.Dept_ID.Dept_ID,
#                 "Dept_Descr": data.Emp_Up_ID.Dept_ID.Dept_Descr,
#                 "Marital_Status": data.Emp_ID.Marital_Status,
#                 "No_of_Children": data.Emp_Up_ID.No_of_Children,
#                 "Transfer_Type": data.Emp_Up_ID.Transfer_Type,
#                 "Account_No": data.Emp_Up_ID.Account_No,
#                 "Bank_Name": data.Emp_Up_ID.Bank_Name,
#                 "Stop_Salary": data.Emp_Up_ID.Stop_Salary,
#                 'Payroll_ID': data.Payroll_ID.PAYROLL_ID,
#                 'Payroll_Name': f'{data.Payroll_ID.MNTH_ID.MNTH_NAME} {data.Payroll_ID.FYID.FinYear}',
#             }
#             datas.append(item)
#         print("DAtas: ", datas)
#         print("DAtas count: ", len(datas))
#         return Response(datas, status=status.HTTP_200_OK)
#     except HR_Emp_Monthly_Sal_Dtl.DoesNotExist:
#         return Response({'error': 'Salary not found'}, status=status.HTTP_404_NOT_FOUND)
#     except Exception as e:
#         return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# @api_view(['GET'])
# def getll_master(request):
#     try:
#         querySet = HR_Emp_Monthly_Sal_Mstr.objects.filter(Payroll_ID__PERIOD_STATUS=True).prefetch_related('Emp_ID', 'Grade_ID', 'Dept_ID', 'Dsg_ID')
       
#         print('querySet: ', querySet.count())
#         datas = []
#         for item in querySet:
#             data = {
#                 'Emp_Up_ID': item.Emp_Up_ID,
#                 'Emp_Up_Date': item.Emp_Up_Date,
#                 'Emp_ID': item.Emp_ID.Emp_ID,
#                 'HR_Emp_ID': item.Emp_ID.HR_Emp_ID,
#                 'Emp_Name': item.Emp_ID.Emp_Name,
#                 'Dsg_Descr': item.Dsg_ID.DSG_Descr,
#                 'Dept_Descr': item.Dept_ID.Dept_Descr
#             }
#             datas.append(data)
#         # print('datas: ', datas)
#         return Response(datas, status=status.HTTP_200_OK)
#     except Exception as e:
#         return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

from monthly_sal_process.models import *

@api_view(['GET'])
def getall_master(request, payroll_id):
    try:
        # Step 1: Get the maximum Emp_Up_ID for each employee
        # latest_salary_updates = HR_Emp_Monthly_Sal_Mstr.objects.values('Emp_ID').annotate(
        #     max_emp_up_id=Max('Emp_Up_ID')
        # )

        # # Step 2: Fetch only the latest records using the maximum Emp_Up_ID values
        # latest_records = HR_Emp_Monthly_Sal_Mstr.objects.filter(
        #     Emp_Up_ID__in=[item['max_emp_up_id'] for item in latest_salary_updates]
        # ).select_related('Emp_ID', 'Dsg_ID', 'Dept_ID')
        # payroll_id = 2
        print('getll_master payroll_id: ', payroll_id)
        datas = []
        if payroll_id:
            latest_records = HR_Emp_Monthly_Sal_Mstr.objects.filter(Payroll_ID=payroll_id).select_related('Emp_ID', 'Dsg_ID', 'Dept_ID')

            print('latest_records count: ', latest_records.count())

            for item in latest_records:
                data = {
                    'Emp_Up_ID': item.Emp_Up_ID,
                    'Emp_Up_Date': item.Emp_Up_Date,
                    'Emp_ID': item.Emp_ID.Emp_ID,
                    'HR_Emp_ID': item.Emp_ID.HR_Emp_ID,
                    'Emp_Name': item.Emp_ID.Emp_Name,
                    'Dsg_Descr': item.Dsg_ID.DSG_Descr,
                    'Dept_Descr': item.Dept_ID.Dept_Descr
                }
                datas.append(data)

            # print('datas: ', datas)
        return Response(datas, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



