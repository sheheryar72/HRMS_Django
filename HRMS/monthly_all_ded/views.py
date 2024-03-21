from django.shortcuts import render
from working_dept_assignment.models import HR_W_All_Ded_Department
from employee.models import HR_Employees
from payroll_element.models import HR_Payroll_Elements
from rest_framework.response import Response
from django.http import JsonResponse
import pdb
from department.models import HR_Department

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











