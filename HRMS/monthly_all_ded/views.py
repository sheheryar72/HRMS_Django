from django.shortcuts import render
from working_dept_assignment.models import HR_W_All_Ded_Department
from employee.models import HR_Employees
from payroll_element.models import HR_Payroll_Elements
from rest_framework.response import Response
from django.http import JsonResponse
import pdb
from department.models import HR_Department
from payroll_period.models import HR_PAYROLL_PERIOD
from django.db.models import F

def Index(request):
    return render(request, 'monthly_all_ded.html')

def getAll_W_Dept_By_DeptID(request, W_DeptID, DeptID):
    print("W_DeptID: ", W_DeptID)
    print("DeptID: ", DeptID)
    try:
        # pdb.set_trace()
        print('getAll_W_Dept_By_DeptID called')
        w_dept_queryset = HR_W_All_Ded_Department.objects.filter(W_All_Ded_Dept_ID=W_DeptID, Dept_ID=DeptID).prefetch_related('W_All_Ded_Dept_ID', 'W_All_Ded_Element_ID', 'Dept_ID')
        # print('w_dept_queryset: ', w_dept_queryset)
        emp_queryset = HR_Employees.objects.filter(Joining_Dept_ID=DeptID)
        data = []
        data2 = []
        for item in emp_queryset:
            single_emp = {
                'Emp_ID': item.Emp_ID,
                'Emp_Name': item.Emp_Name
            }
            data.append(single_emp)

            # print('Employee data: ', data)

        for item in w_dept_queryset:
            single_w_dept = {
                'Element_ID': item.W_All_Ded_Element_ID.Element_ID,
                'Element_Name': item.W_All_Ded_Element_ID.Element_Name
            }
            data2.append(single_w_dept)

            # print('Element data2: ', data2)

        data3 = []

        data3.append({"Employee": data})
        data3.append({"Element": data2})
        print('data3: ', data3)

        # print('data3: ', data3)
        # return Response(data3, status=200)
        return JsonResponse(data3, safe=False)
    except Exception as e:
        return Response({'error': str(e)}, status=500)

def getAll_Assigned_Dept(request, DeptID):
    try:
        dept_ids = HR_W_All_Ded_Department.objects.filter(W_All_Ded_Dept_ID=DeptID).values_list("Dept_ID", flat=True).distinct()

        dept_instance = HR_Department.objects.filter(Dept_ID__in=dept_ids)

        data = []
        for dept in dept_instance:
            single_dept = {
                'Dept_ID': dept.Dept_ID,
                'Dept_Descr': dept.Dept_Descr,
            }
            data.append(single_dept)
        return JsonResponse(data, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, safe=False)

def getAll_W_Dept_By_W_DeptID(request, W_DeptID, DeptID):
    try:
        dept_ids = HR_W_All_Ded_Department.objects.filter(W_All_Ded_Dept_ID=W_DeptID, Dept_ID=DeptID).values_list('Dept_ID', flat=True)

        emp_queryset = HR_Employees.objects.filter(Joining_Dept_ID__in=dept_ids)

        employees_data = [{'Emp_ID': emp.Emp_ID, 'Emp_Name': emp.Emp_Name} for emp in emp_queryset]

        elements_queryset = HR_W_All_Ded_Department.objects.filter(W_All_Ded_Dept_ID=W_DeptID, Dept_ID=DeptID).values('W_All_Ded_Element_ID__Element_ID', 'W_All_Ded_Element_ID__Element_Name').distinct()

        elements_data = [{'Element_ID': elem['W_All_Ded_Element_ID__Element_ID'], 'Element_Name': elem['W_All_Ded_Element_ID__Element_Name']} for elem in elements_queryset]

        dept_queryset = HR_Department.objects.get(Dept_ID=W_DeptID)
        dept_data = {'Dept_ID': dept_queryset.Dept_ID, 'Dept_Descr': dept_queryset.Dept_Descr}

        payroll_period_queryset = HR_PAYROLL_PERIOD.objects.filter(PERIOD_STATUS=True).values('ID', 'MNTH_ID__MNTH_ID', 'MNTH_ID__MNTH_NAME').first()
        payroll_period = {'ID': payroll_period_queryset['ID'], 'MNTH_ID': payroll_period_queryset['MNTH_ID__MNTH_ID'], 'MNTH_NAME': payroll_period_queryset['MNTH_ID__MNTH_NAME']}

        response_data = {'Employee': employees_data, 'Element': elements_data, 'Period': payroll_period, 'Department': dept_data}
        return JsonResponse(response_data, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


# def getAll_W_Dept_By_W_DeptID(request, W_DeptID):
#     try:
#         # Get all department IDs associated with the given W_DeptID
#         dept_ids = HR_W_All_Ded_Department.objects.filter(W_All_Ded_Dept_ID=W_DeptID).values_list('Dept_ID', flat=True)

#         # Get all employees in departments with the retrieved department IDs
#         emp_queryset = HR_Employees.objects.filter(Joining_Dept_ID__in=dept_ids)

#         # Create a list of dictionaries containing employee data
#         employees_data = [{'Emp_ID': emp.Emp_ID, 'Emp_Name': emp.Emp_Name} for emp in emp_queryset]

#         # Get distinct elements associated with the retrieved department IDs
#         elements_queryset = HR_W_All_Ded_Department.objects.filter(W_All_Ded_Dept_ID=W_DeptID).values_list('W_All_Ded_Element_ID__Element_ID', 'W_All_Ded_Element_ID__Element_Name').distinct()

#         # Create a list of dictionaries containing element data
#         elements_data = [{'Element_ID': elem[0], 'Element_Name': elem[1]} for elem in elements_queryset]

#         payroll_period_queryset = HR_PAYROLL_PERIOD.objects.filter(PERIOD_STATUS=True).values('ID', 'MNTH_ID__MNTH_ID', 'MNTH_ID__MNTH_NAME')
        
#         # payroll_period_queryset = HR_PAYROLL_PERIOD.objects.filter(PERIOD_STATUS=True).values('ID', 'MNTH_ID__MNTH_ID', 'MNTH_ID__MNTH_NAME').annotate(
#         # MNTH_ID=F('MNTH_ID__MNTH_ID'),
#         # MNTH_NAME=F('MNTH_ID__MNTH_NAME'))

#         # print('payroll_period_queryset: ', payroll_period_queryset)

#         dept_queryset = HR_Department.objects.get(Dept_ID=W_DeptID)

#         print('dept_queryset: ', dept_queryset)

#         dept_data = {'Dept_ID': dept_queryset['Dept_ID'], 'Dept_Descr': dept_queryset['Dept_Descr']}

#         payroll_period = {'ID': payroll_period_queryset[0]['ID'], 'MNTH_ID': payroll_period_queryset[0]['MNTH_ID__MNTH_ID'], 'MNTH_NAME': payroll_period_queryset[0]['MNTH_ID__MNTH_NAME']}

#         # Prepare the response data
#         response_data = {'Employee': employees_data, 'Element': elements_data, 'Period': payroll_period, 'Department': dept_data}
#         print('response_data Elements: ', response_data['Element'])
#         return JsonResponse(response_data, safe=False)
#     except Exception as e:
#         return JsonResponse({'error': str(e)}, status=500)


def getAll_W_Dept_By_W_DeptID(request, W_DeptID):
    try:
        # Get all department IDs associated with the given W_DeptID
        dept_ids = HR_W_All_Ded_Department.objects.filter(W_All_Ded_Dept_ID=W_DeptID).values_list('Dept_ID', flat=True)

        # Get all employees in departments with the retrieved department IDs
        emp_queryset = HR_Employees.objects.filter(Joining_Dept_ID__in=dept_ids)

        # Create a list of dictionaries containing employee data
        employees_data = [{'Emp_ID': emp.Emp_ID, 'Emp_Name': emp.Emp_Name} for emp in emp_queryset]

        # Get distinct elements associated with the retrieved department IDs
        elements_queryset = HR_W_All_Ded_Department.objects.filter(W_All_Ded_Dept_ID=W_DeptID).values('W_All_Ded_Element_ID__Element_ID', 'W_All_Ded_Element_ID__Element_Name').distinct()

        # Create a list of dictionaries containing element data
        elements_data = [{'Element_ID': elem['W_All_Ded_Element_ID__Element_ID'], 'Element_Name': elem['W_All_Ded_Element_ID__Element_Name']} for elem in elements_queryset]

        # Get department details
        dept_queryset = HR_Department.objects.get(Dept_ID=W_DeptID)
        dept_data = {'Dept_ID': dept_queryset.Dept_ID, 'Dept_Descr': dept_queryset.Dept_Descr}

        # Get payroll period details
        payroll_period_queryset = HR_PAYROLL_PERIOD.objects.filter(PERIOD_STATUS=True).values('ID', 'MNTH_ID__MNTH_ID', 'MNTH_ID__MNTH_NAME').first()
        payroll_period = {'ID': payroll_period_queryset['ID'], 'MNTH_ID': payroll_period_queryset['MNTH_ID__MNTH_ID'], 'MNTH_NAME': payroll_period_queryset['MNTH_ID__MNTH_NAME']}

        # Prepare the response data
        response_data = {'Employee': employees_data, 'Element': elements_data, 'Period': payroll_period, 'Department': dept_data}
        return JsonResponse(response_data, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)



