from django.shortcuts import render
from .models import HR_MONTHLY_PAY_SHEET
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from monthly_all_ded.models import HR_Monthly_All_Ded
from django.db import transaction
from django.db.models.functions import Coalesce
from django.db import transaction
from django.http import HttpResponse
import requests

def payroll_sheet_view(request):
    return render(request=request, template_name='payrollsheet.html')


def execute_monthly_pay_sheet(request, payroll_id):
    print('execute_salary_process')
    api_url = 'https://localhost:44339/api/SalaryUpdate/ExecuteMonthlyPaySheet'
    params = {
        'Payroll_ID': payroll_id
    }
    headers = {
        'Authorization': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJVc2VyX0lEIjoiMiIsIm5iZiI6MTcyMjYyMjMzMiwiZXhwIjoxNzIzMjI3MTMyLCJpYXQiOjE3MjI2MjIzMzJ9._yFPxWiBp8EZJk5YBdj3VIKXjuNXLk_JAwbtKxBiFLA'
    }

    try:
        # response = requests.get(api_url, params=params, headers=headers, verify=False)

        # response = {
        #     'status_code': 200
        # }

        response_status_code = 200

        if response_status_code == 200:
            data = []

            # Retrieve all records from HR_MONTHLY_PAY_SHEET
            records = HR_MONTHLY_PAY_SHEET.objects.select_related('Emp_ID', 'Payroll_ID', 'Dept_ID')[:20]

            # Map fields to dictionary for each record
            for record in records:
                data.append({
                    # 'Emp_Up_ID': record.Emp_Up_ID,
                    # 'Emp_ID': record.Emp_ID.Emp_ID,
                    'HR_Emp_ID': record.Emp_ID.HR_Emp_ID,
                    'Emp_Name': record.Emp_ID.Emp_Name,
                    # 'Dept_ID': record.Dept_ID.Dept_ID,
                    'Dept_Descr': record.Dept_ID.Dept_Descr,
                    # 'DSG_ID': record.Emp_ID.Joining_Dsg_ID.DSG_ID,
                    'DSG_Descr': record.Emp_ID.Joining_Dsg_ID.DSG_Descr,
                    'CT_Descr': record.Emp_ID.CT_ID.CT_Descr,
                    'REG_Descr': record.Emp_ID.REG_ID.REG_Descr,
                    'Emp_Status': record.Emp_ID.Emp_Status,
                    'DateOfBirth': record.Emp_ID.DateOfBirth,
                    'CNIC_No': record.Emp_ID.CNIC_No,
                    'Payroll_ID': record.Payroll_ID.PAYROLL_ID,
                    'MDays': record.MDays,
                    'WDAYS': record.WDAYS,
                    'ADAYS': record.ADAYS,
                    'JLDAYS': record.JLDAYS,
                    'Basic_Salary_1': record.Basic_Salary_1,
                    'Medical_Allowance_2': record.Medical_Allowance_2,
                    'Conveyance_Allowance_3': record.Conveyance_Fixed_Allowance_3,
                    'Overtime_Allowansce_4': record.Overtime_Allowance_4,
                    'House_Rent_Allowanc_5': record.House_Rent_Allowance_5,
                    'Utilities_Allowance_6': record.Utilities_Allowance_6,
                    'Meal_Allowance_7': record.Meal_Allowance_7,
                    'Arrears_8': record.Arrears_8,
                    'Bike_Maintainence_9': record.Bike_Maintainence_9,
                    'Incentives_10': record.Incentives_Tech_10,
                    'Device_Reimbursment_11': record.Device_Reimbursment_11,
                    'Communication_12': record.Communication_12,
                    'Bonus_13': record.Incentives_KPI_13,
                    'Other_Allowance_14': record.Other_Allowance_14,
                    'Loan_15': record.Loan_15,
                    'Advance_Salary_16': record.Advance_Salary_16,
                    'EOBI_17': record.EOBI_17,
                    'Income_Tax_18': record.Income_Tax_18,
                    'Absent_Days_19': record.Absent_Days_19,
                    'Device_Deduction_20': record.Device_Deduction_20,
                    'Over_Utilizaton_Mobile_21': record.Over_Utilization_Mobile_21,
                    'Vehicle_or_Fuel_Deduction_22': record.Vehicle_Fuel_Deduction_22,
                    'Pandamic_Deduction_23': record.Pandamic_Deduction_23,
                    'Late_Days_24': record.Late_Days_24,
                    'Other_Deduction_25': record.Other_Deduction_25,
                    'Mobile_Installment_26': record.Mobile_Installment_26,
                    'Food_Panda_27': record.Food_Panda_27,
                    'Conveyance_Liters_Allowance_28': record.Conveyance_Liters_Allowance_28,
                })

                print('pay sheet data: ', data)

            return JsonResponse({
                'ResponseCode': response_status_code,
                'Message': 'Successfully executed',
                'Data': data
            })
        else:
            return JsonResponse({
                'ResponseCode': response_status_code,
                'Message': 'Failed to execute external API',
                'Data': None
            })
    except requests.RequestException as e:
        return JsonResponse({
            'ResponseCode': 500,
            'Message': f'Error occurred: {str(e)}',
            'Data': None
        })




# api_view(['get_payrollsheet'])
# def get_payrollsheet(request, payroll_id):
#     try:
#         monthly_payroll_sheet = HR_MONTHLY_PAY_SHEET.objects.filter(Payroll_ID=payroll_id).select_related(
#             'Emp_ID', 'Emp_Up_ID', 'Dept_ID', 'Payroll_ID'
#         )

#         if not monthly_payroll_sheet.exists():
#             return Response({
#                 'ResponseCode': 404,
#                 'Message': 'No records found for the provided payroll ID',
#                 'Data': None
#             }, status=404)

#         data = []
#         for record in monthly_payroll_sheet:
#             data.append({
#                 'HR_Emp_ID': record.Emp_ID.HR_Emp_ID if record.Emp_ID else None,
#                 'Emp_Name': record.Emp_ID.Emp_Name if record.Emp_ID else None,
#                 'Designation': record.Emp_ID.Joining_Dsg_ID.DSG_Descr if record.Emp_ID else None,
#                 'Department': record.Dept_ID.Dept_Descr if record.Dept_ID else None,  
#                 'MNTH_NAME': record.Payroll_ID.MNTH_ID.MNTH_NAME if record.Payroll_ID else None, 
#                 'FinYear': record.Payroll_ID.FYID.FinYear if record.Payroll_ID else None, 
#                 'MDays': record.MDays,
#                 'WDAYS': record.WDAYS,
#                 'ADAYS': record.ADAYS,
#                 'JLDAYS': record.JLDAYS,
#                 'Basic_Salary_1': record.Basic_Salary_1,
#                 'Medical_Allowance_2': record.Medical_Allowance_2,
#                 'Conveyance_Allowance_3': record.Conveyance_Allowance_3,
#                 'Overtime_Allowansce_4': record.Overtime_Allowansce_4,
#                 'House_Rent_Allowanc_5': record.House_Rent_Allowanc_5,
#                 'Utilities_Allowance_6': record.Utilities_Allowance_6,
#                 'Meal_Allowance_7': record.Meal_Allowance_7,
#                 'Arrears_8': record.Arrears_8,
#                 'Bike_Maintainence_9': record.Bike_Maintainence_9,
#                 'Incentives_10': record.Incentives_10,
#                 'Device_Reimbursment_11': record.Device_Reimbursment_11,
#                 'Communication_12': record.Communication_12,
#                 'Bonus_13': record.Bonus_13,
#                 'Other_Allowance_14': record.Other_Allowance_14,
#                 'Loan_15': record.Loan_15,
#                 'Advance_Salary_16': record.Advance_Salary_16,
#                 'EOBI_17': record.EOBI_17,
#                 'Income_Tax_18': record.Income_Tax_18,
#                 'Absent_Days_19': record.Absent_Days_19,
#                 'Device_Deduction_20': record.Device_Deduction_20,
#                 'Over_Utilizaton_Mobile_21': record.Over_Utilizaton_Mobile_21,
#                 'Vehicle_or_Fuel_Deduction_22': record.Vehicle_or_Fuel_Deduction_22,
#                 'Pandamic_Deduction_23': record.Pandamic_Deduction_23,
#                 'Late_Days_24': record.Late_Days_24,
#                 'Other_Deduction_25': record.Other_Deduction_25,
#                 'Mobile_Installment_26': record.Mobile_Installment_26,
#                 'Food_Panda_27': record.Food_Panda_27,
#             })

#         return Response({
#             'ResponseCode': 200,
#             'Message': 'Successfully retrieved payroll sheet data',
#             'Data': data
#         }, safe=False, status=200)

#     except Exception as e:
#         return Response(f"Error occurred while fetching payroll sheet: {str(e)}", status=500)


# @api_view(['POST'])
# def insert_data_from_all_ded_to_pay_sheet(request, payroll_id):
    
#     if not payroll_id:
#         return Response({
#             'ResponseCode': 400,
#             'Message': 'Payroll ID is required',
#             'Data': None
#         }, status=400)

#     try:
#         records = HR_Monthly_All_Ded.objects.filter(Period__PAYROLL_ID=payroll_id)

#         if not records.exists():
#             return Response({
#                 'ResponseCode': 404,
#                 'Message': 'No records found for the provided payroll ID',
#                 'Data': None
#             }, status=404)

#         with transaction.atomic():  
#             for record in records:
#                 HR_MONTHLY_PAY_SHEET.objects.update_or_create(
#                     Emp_ID=record.Employee,
#                     Payroll_ID=record.Period,
#                     defaults={
#                         'Emp_Up_ID': record.Employee,  
#                         'Dept_ID': record.Department,
#                         'MDays': 0,  
#                         'WDAYS': 0,
#                         'ADAYS': 0,
#                         'JLDAYS': 0,
#                         'Basic_Salary_1': record.Basic_Salary_1,
#                         'Medical_Allowance_2': record.Medical_Allowance_2,
#                         'Conveyance_Allowance_3': record.Conveyance_Allowance_3,
#                         'Overtime_Allowansce_4': record.Overtime_Allowansce_4,
#                         'House_Rent_Allowanc_5': record.House_Rent_Allowanc_5,
#                         'Utilities_Allowance_6': record.Utilities_Allowance_6,
#                         'Meal_Allowance_7': record.Meal_Allowance_7,
#                         'Arrears_8': record.Arrears_8,
#                         'Bike_Maintainence_9': record.Bike_Maintainence_9,
#                         'Incentives_10': record.Incentives_10,
#                         'Device_Reimbursment_11': record.Device_Reimbursment_11,
#                         'Communication_12': record.Communication_12,
#                         'Bonus_13': record.Bonus_13,
#                         'Other_Allowance_14': record.Other_Allowance_14,
#                         'Loan_15': record.Loan_15,
#                         'Advance_Salary_16': record.Advance_Salary_16,
#                         'EOBI_17': record.EOBI_17,
#                         'Income_Tax_18': record.Income_Tax_18,
#                         'Absent_Days_19': record.Absent_Days_19,
#                         'Device_Deduction_20': record.Device_Deduction_20,
#                         'Over_Utilizaton_Mobile_21': record.Over_Utilizaton_Mobile_21,
#                         'Vehicle_or_Fuel_Deduction_22': record.Vehicle_or_Fuel_Deduction_22,
#                         'Pandamic_Deduction_23': record.Pandamic_Deduction_23,
#                         'Late_Days_24': record.Late_Days_24,
#                         'Other_Deduction_25': record.Other_Deduction_25,
#                         'Mobile_Installment_26': record.Mobile_Installment_26,
#                         'Food_Panda_27': record.Food_Panda_27
#                     }
#                 )

#         return Response({
#             'ResponseCode': 200,
#             'Message': 'Data successfully inserted into HR_MONTHLY_PAY_SHEET',
#             'Data': None
#         }, status=200)

#     except Exception as e:
#         return Response({
#             'ResponseCode': 500,
#             'Message': f'An error occurred: {str(e)}',
#             'Data': None
#         }, status=500)

