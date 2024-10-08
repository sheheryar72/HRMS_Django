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
from .models import HR_Monthly_All_Ded, HR_Emp_Salary_Grade_V
from rest_framework.decorators import api_view
from rest_framework import status
from .serializers import HR_Monthly_All_Ded_Serializer
from django.db.models import Q
from payroll_period.serialiers import HR_PAYROLL_PERIOD_Serializer
from employee.serializers import HR_Employees_Serializer
from salary_update.models import HR_Emp_Sal_Update_Mstr
from .models import HR_Element_Grade_Combination

def Index(request):
    return render(request, 'monthly_all_ded.html')



# def getAll_W_Dept_By_DeptID(request, W_DeptID, DeptID):
#     print("getAll_W_Dept_By_DeptID")
    
#     try:
#         # Fetch relevant data from the database
#         w_dept_queryset = HR_W_All_Ded_Department.objects.filter(
#             W_All_Ded_Dept_ID=W_DeptID,
#             Dept_ID=DeptID
#         ).prefetch_related(
#             'W_All_Ded_Dept_ID', 'W_All_Ded_Element_ID', 'Dept_ID'
#         )
        
#         emp_queryset = HR_Emp_Salary_Grade_V.objects.filter(
#             Dept_ID=DeptID
#         ).distinct()

#         month_pp_queryset = HR_Monthly_All_Ded.objects.filter(
#             Department=DeptID
#         )

#         month_pp_serializer = HR_Monthly_All_Ded_Serializer(
#             month_pp_queryset, many=True
#         )

#         # Convert serialized data to a dictionary for quick lookup by Emp_ID
#         month_pp_data = {item['Employee']: item['Element_Amount'] for item in month_pp_serializer.data}

#         # Prepare the data for response
#         data = []
#         data2 = []
#         data4 = []

#         for item in emp_queryset:
#             element_amount = month_pp_data.get(item.Emp_ID, [])  # Use .get() to handle cases where Emp_ID might not be present

#             single_emp = {
#                 'Emp_ID': item.Emp_ID,
#                 'Emp_Name': item.Emp_Name,
#                 'HR_Emp_ID': item.HR_Emp_ID,
#                 'Grade_ID': item.Grade_ID,
#                 'Grade_Descr': item.Grade_Descr,
#                 'Element_Amount': element_amount
#             }

#             data.append(single_emp)

#             a1 = w_dept_queryset.values_list('W_All_Ded_Element_ID__Element_ID', flat=True).distinct()
#             grade_comb = HR_Element_Grade_Combination.objects.filter(
#                 Grade_ID=item.Grade_ID,
#                 Element_ID__in=a1
#             )
            
#             for j in grade_comb:
#                 data4.append({
#                     'Emp_ID': item.Emp_ID,
#                     'Element_ID': j.Element_ID.Element_ID,
#                     'Grade_ID': j.Grade_ID.Grade_ID
#                 })

#         for item in w_dept_queryset:
#             single_w_dept = {
#                 'Element_ID': item.W_All_Ded_Element_ID.Element_ID,
#                 'Element_Name': item.W_All_Ded_Element_ID.Element_Name
#             }
#             data2.append(single_w_dept)

#         data3 = [
#             {"Employee": data},
#             {"Element": data2},
#             {"Emp_Element_Status": data4}
#         ]

#         return JsonResponse(data3, safe=False)
    
#     except Exception as e:
#         print(f"Error: {str(e)}")  
#         return JsonResponse({'error': str(e)}, status=500)



def getAll_W_Dept_By_DeptID(request, W_DeptID, DeptID, Payroll_ID):
    print("getAll_W_Dept_By_DeptID")
    
    try:
        # Fetch relevant data from the database
        w_dept_queryset = HR_W_All_Ded_Department.objects.filter(
            W_All_Ded_Dept_ID=W_DeptID,
            Dept_ID=DeptID
        ).prefetch_related(
            'W_All_Ded_Dept_ID', 'W_All_Ded_Element_ID', 'Dept_ID'
        )
        
        # print('w_dept_queryset: ', w_dept_queryset)c

        emp_queryset = HR_Emp_Salary_Grade_V.objects.filter(
            Dept_ID=DeptID
        ).distinct()

        print('emp_queryset: ', emp_queryset.__dict__)

        month_pp_queryset = HR_Monthly_All_Ded.objects.filter(
            Department=DeptID,
            Period=Payroll_ID
        )

        print('month_pp_queryset: ', month_pp_queryset.__dict__)

        # print('month_pp_queryset: ', month_pp_queryset)

        month_pp_serializer = HR_Monthly_All_Ded_Serializer(
            month_pp_queryset, many=True
        )

        # print('month_pp_serializer: ', month_pp_serializer.data)

        for item in month_pp_serializer.data:
            print('month_pp_serializer item: ', item)

        # print('count 1: ', emp_queryset.count())
        # print('count 2: ', month_pp_queryset.count())
        # print('count 3: ', w_dept_queryset.count())

        # print('count 1: ', emp_queryset)
        # print('count 2: ', month_pp_queryset)
        # print('count 3: ', w_dept_queryset)

        # Prepare the data for response
        data = []
        data2 = []
        data4 = []

        count = 0
        for item in emp_queryset:

            matching_employee_data = next(
                (entry for entry in month_pp_serializer.data if entry['Employee'] == item.Emp_ID),
                None
                )
            single_emp = {
                'Emp_ID': item.Emp_ID,
                'Emp_Name': item.Emp_Name,
                'HR_Emp_ID': item.HR_Emp_ID,
                'Grade_ID': item.Grade_ID,
                'Grade_Descr': item.Grade_Descr,
                'Element_Amount': matching_employee_data if matching_employee_data else []
                # 'Element_Amount': month_pp_serializer.data[item.Emp_ID] if count < len(month_pp_serializer.data) else []
                # 'Element_Amount': month_pp_serializer.data[count] if count < len(month_pp_serializer.data) else []
            }

            count += 1
            data.append(single_emp)

            # print('Employee data: ', data)

            a1 = w_dept_queryset.values_list('W_All_Ded_Element_ID__Element_ID', flat=True).distinct()
            grade_comb = HR_Element_Grade_Combination.objects.filter(
                Grade_ID=item.Grade_ID,
                Element_ID__in=a1
            )
            
            for j in grade_comb:
                data4.append({
                    'Emp_ID': item.Emp_ID,
                    'Element_ID': j.Element_ID.Element_ID,
                    'Grade_ID': j.Grade_ID.Grade_ID
                })

        # print('data4: ', data4)

        for item in w_dept_queryset:
            single_w_dept = {
                'Element_ID': item.W_All_Ded_Element_ID.Element_ID,
                'Element_Name': item.W_All_Ded_Element_ID.Element_Name
            }
            data2.append(single_w_dept)

        data3 = [
            {"Employee": data},
            {"Element": data2},
            {"Emp_Element_Status": data4}
        ]

        return JsonResponse(data3, safe=False)
    
    except Exception as e:
        print(f"Error: {str(e)}")  
        return JsonResponse({'error': str(e)}, status=500)


# def getAll_W_Dept_By_DeptID(request, W_DeptID, DeptID):
#     # print("W_DeptID: ", W_DeptID)
#     # print("DeptID: ", DeptID)
#     print("getAll_W_Dept_By_DeptID")
#     try:
#         # pdb.set_trace()
#         # print('getAll_W_Dept_By_DeptID called')
#         w_dept_queryset = HR_W_All_Ded_Department.objects.filter(W_All_Ded_Dept_ID=W_DeptID, Dept_ID=DeptID).prefetch_related('W_All_Ded_Dept_ID', 'W_All_Ded_Element_ID', 'Dept_ID')
#         # print('w_dept_queryset: ', w_dept_queryset)
#         # emp_queryset = HR_Employees.objects.filter(Joining_Dept_ID=DeptID)
        
#         # emp_queryset = HR_Emp_Sal_Update_Mstr.objects.filter(Dept_ID=DeptID).select_related("Emp_ID")

#         emp_queryset = HR_Emp_Salary_Grade_V.objects.filter(Dept_ID=DeptID).distinct()

#         print('emp_queryset: ', emp_queryset)

#         print('deprt: ', DeptID)
        
#         month_pp_queryset = HR_Monthly_All_Ded.objects.filter(Department=DeptID)

#         month_pp_serializer = HR_Monthly_All_Ded_Serializer(month_pp_queryset, many=True)

#         # print('month_pp_serializer: ', month_pp_serializer.data)

#         print('count 1: ', emp_queryset.count())
#         print('count 2: ', month_pp_queryset.count())
#         print('count 3: ', w_dept_queryset.count())

#         data = []
#         data2 = []
#         data4 = []

#         count = 0
#         for item in emp_queryset:
#             single_emp = {
#                 'Emp_ID': item.Emp_ID,
#                 'Emp_Name': item.Emp_Name,
#                 'HR_Emp_ID': item.HR_Emp_ID,
#                 'Grade_ID': item.Grade_ID,
#                 'Grade_Descr': item.Grade_Descr,
#                 # 'Element_Amount': 0
#                 'Element_Amount': month_pp_serializer.data[count] if month_pp_serializer.data else []
#             }

#             # single_emp = {
#             #     'Emp_ID': item.Emp_ID.Emp_ID,
#             #     'Emp_Name': item.Emp_ID.Emp_Name,
#             #     'Element_Amount': month_pp_serializer.data[count] if month_pp_serializer.data else []
#             # }
#             # print('count: ', count)
#             # print('month_pp_serializer: ', month_pp_serializer.data[count])
#             count += 1
#             data.append(single_emp)

#             print('Employee data: ', data)

#             a1 = w_dept_queryset.values_list('W_All_Ded_Element_ID__Element_ID', flat=True).distinct()
#             # print('a1: ', a1)

#             grade_comb = HR_Element_Grade_Combination.objects.filter(Grade_ID=item.Grade_ID, Element_ID__in=a1)
#             # grade_comb = HR_Element_Grade_Combination.objects.filter(Grade_ID=item.Grade_ID, Element_ID__in=(27))
#             # print('grade_comb: ', grade_comb)
#             for j in grade_comb:
#                 data4.append({
#                     'Emp_ID': item.Emp_ID,
#                     'Element_ID': j.Element_ID.Element_ID,
#                     'Grade_ID': j.Grade_ID.Grade_ID,  
#                 })


#         print('data4: ', data4)

#         for item in w_dept_queryset:
#             single_w_dept = {
#                 'Element_ID': item.W_All_Ded_Element_ID.Element_ID,
#                 'Element_Name': item.W_All_Ded_Element_ID.Element_Name
#             }
#             data2.append(single_w_dept)

#             # print('Element data2: ', data2)

#         data3 = []

#         data3.append({"Employee": data})
#         data3.append({"Element": data2})
#         data3.append({"Emp_Element_Status": data4})
#         # data3.append({"Monthly_Payromm_Element": month_pp_serializer.data})

#         # print('data3: ', data3)

#         # print('data3: ', data3)
#         # return Response(data3, status=200)
#         return JsonResponse(data3, safe=False)
#     except Exception as e:
#         return Response({'error': str(e)}, status=500)


def test2(request, W_DeptID, DeptID):
    try:

        elements_name = HR_W_All_Ded_Department.objects.filter(W_All_Ded_Dept_ID=W_DeptID, Dept_ID=DeptID).prefetch_related('W_All_Ded_Element_ID').values_list('W_All_Ded_Element_ID__Element_Name')

        elements_name_list = list(elements_name)
        
        month_pp_queryset = HR_Monthly_All_Ded.objects.filter(Department=DeptID).select_related('Employee', 'Period', 'Department').values(elements_name_list)

        month_pp_serializer = HR_Monthly_All_Ded_Serializer(month_pp_queryset, many=True)

        return JsonResponse(month_pp_serializer.data, safe=False)
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
        payroll_period_queryset = HR_PAYROLL_PERIOD.objects.filter(PERIOD_STATUS=True).values('PAYROLL_ID', 'MNTH_ID__MNTH_ID', 'MNTH_ID__MNTH_NAME', 'FYID__FinYear').first()
        payroll_period = {'PAYROLL_ID': payroll_period_queryset['PAYROLL_ID'], 'MNTH_ID': payroll_period_queryset['MNTH_ID__MNTH_ID'], 'MNTH_NAME': payroll_period_queryset['MNTH_ID__MNTH_NAME'], 'FinYear': payroll_period_queryset['FYID__FinYear']}

        # Prepare the response data
        response_data = {'Employee': employees_data, 'Element': elements_data, 'Period': payroll_period, 'Department': dept_data}
        return JsonResponse(response_data, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
@api_view(['GET'])
def get_current_pp(request):
    try:
        pp_instance = HR_PAYROLL_PERIOD.objects.get(PERIOD_STATUS=True)
        print('pp_instance: ', pp_instance)
        data = {}
        data["PERIOD_ID"] = pp_instance.PAYROLL_ID
        data["MNTH_NAME"] = pp_instance.MNTH_ID.MNTH_NAME
        data["FinYear"] = pp_instance.FYID.FinYear
        # pp_serializer = HR_PAYROLL_PERIOD_Serializer(pp_instance)
        print('get_current_pp: ', data)
        return Response(data, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@api_view(['POST'])
def Insert_Monthly_PE(request):
    try:
        table_data = request.data['table_data']
        W_Department = request.data['W_Department']
        print('table_data: ', table_data)

        for item in table_data:
            # print('item: ', item)
            # print('item.Employee: ', item['Employee'])
            my_monthly_data = {}
            my_monthly_data['Employee'] = item['Employee']
            my_monthly_data['Period'] = item["Period"]
            my_monthly_data['Department'] = W_Department
            for key, value in item.items():
                # print('Key:', key)
                # print('Value:', value)
                my_monthly_data[key] = value

            # Check if data already exists
            existing_data = HR_Monthly_All_Ded.objects.filter(Employee=my_monthly_data['Employee'], Period=my_monthly_data['Period'])
            if existing_data.exists():
                # Update existing data
                serializer = HR_Monthly_All_Ded_Serializer(existing_data.first(), data=my_monthly_data)
            else:
                # Create new data
                serializer = HR_Monthly_All_Ded_Serializer(data=my_monthly_data)
            
            if serializer.is_valid():
                serializer.save()
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({'message': 'Data saved successfully'}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# @api_view(['POST'])
# def Insert_from_excel(request):
#     W_Department = request.data.get("W_Department")
#     table_data = request.data.get("table_data")
#     period = request.data.get('Period')
#     print('W_Department: ', W_Department)
#     print('table_data: ', table_data)
#     print('period: ', period)
#     print('table_data type: ', type(table_data))
#     for i in range(len(table_data)):
#         print('obj: ', table_data['Emp_ID'][i])
#         existing_data = HR_Monthly_All_Ded.objects.filter(Employee=table_data['Emp_ID'][i], Period=period, Department=W_Department)
#         if existing_data.exists():
#             serializer = HR_Monthly_All_Ded_Serializer(existing_data.first(), data=my_monthly_data)
#             serializer.save()


# @api_view(['POST'])
# def Insert_from_excel(request):
#     try:
#         W_Department = request.data.get("W_Department")
#         table_data = request.data.get("table_data")
#         period = request.data.get('Period')
#         # print('W_Department: ', W_Department)
#         print('table_data: ', table_data)
#         print('period: ', period)
#         # print('table_data type: ', type(table_data))

#         # Assuming 'Emp_ID' is a key in table_data and it contains an array
#         if 'Emp_ID' in table_data:
#             for i in range(len(table_data['Emp_ID'])):
#                 emp_id = table_data['Emp_ID'][i]

#                 # Prepare data dictionary for serialization
#                 my_monthly_data = {
#                     'Employee': int(emp_id),
#                     'Period': int(period),
#                     'Department': int(W_Department),
#                 }

#                 # Dynamically add other columns from table_data
#                 for key, value in table_data.items():
#                     if key != 'Emp_ID' and i < len(value) and key != 'Emp_Name':
#                         my_monthly_data[key] = int(value[i])

#                 # Use the values to perform your operations
#                 print('my_monthly_data: ', my_monthly_data)
#                 existing_data = HR_Monthly_All_Ded.objects.filter(Employee=emp_id, Period=period, Department=W_Department)
#                 if existing_data.exists():
#                     serializer = HR_Monthly_All_Ded_Serializer(existing_data.first(), data=my_monthly_data)
#                 else:
#                     serializer = HR_Monthly_All_Ded_Serializer(data=my_monthly_data)

#                 if serializer.is_valid():
#                     serializer.save()
#                 else:
#                     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#         return Response({'message': 'Data saved successfully'}, status=status.HTTP_200_OK)
#     except Exception as e:
#         return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def Insert_from_excel(request):
    try:
        W_Department = request.data.get("W_Department")
        table_data = request.data.get("table_data")
        period = request.data.get('Period')
        print('W_Department: ', W_Department)
        print('table_data: ', table_data)
        print('period: ', period)

        if 'Emp_ID' in table_data:
            for i in range(len(table_data['Emp_ID'])):
                emp_id = table_data['Emp_ID'][i]
                my_monthly_data = {
                    'Employee': int(emp_id),
                    'Period': int(period),
                    'Department': int(W_Department),
                }

                for key, value in table_data.items():
                    print('key: ', key, ' value: ', value[i])
                    if key != 'Emp_ID' and i < len(value) and key != 'HR_Emp_ID' and key != 'Emp_Name' and key != 'Department' and key != 'Designation':
                        try:
                            my_monthly_data[key] = int(value[i]) if value[i] is not None else 0
                        except ValueError:
                            my_monthly_data[key] = 0  # Set to None if conversion fails

                        # try:
                        #     # Convert to int or default to 0 if value is None
                        #     my_monthly_data[key] = int(value[i]) if value[i] is not None else 0
                        # except (ValueError, TypeError) as e:
                        #     print(f"Error converting {value[i]} to int for key {key}: {e}")
                        #     my_monthly_data[key] = 0  # Default to 0 in case of error

                print('my_monthly_data: ', my_monthly_data)
                existing_data = HR_Monthly_All_Ded.objects.filter(Employee=emp_id, Period=period, Department=W_Department)
                if existing_data.exists():
                    serializer = HR_Monthly_All_Ded_Serializer(existing_data.first(), data=my_monthly_data)
                else: 
                    serializer = HR_Monthly_All_Ded_Serializer(data=my_monthly_data)

                if serializer.is_valid():
                    serializer.save()
                else:
                    print('Serializer errors:', serializer.errors)  # Print serializer errors for debugging
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({'message': 'Data saved successfully'}, status=status.HTTP_200_OK)
    except Exception as e:
        print('Exception:', e)  # Print the exception for debugging
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

from django.db.models import Max, OuterRef, Subquery

@api_view(['GET'])
def export_template(request, ID):
    try:
        assigned_depts = HR_W_All_Ded_Department.objects.filter(W_All_Ded_Dept_ID=ID).values_list('Dept_ID', flat=True)

        # Get the max Emp_Up_ID per employee in each department
        max_emp_up_id_subquery = HR_Emp_Sal_Update_Mstr.objects.filter(
        Emp_ID=OuterRef('Emp_ID'),
        Dept_ID__in=assigned_depts
        ).values('Emp_ID').annotate(max_id=Max('Emp_Up_ID')).values('max_id')

        # assigned_depts = HR_W_All_Ded_Department.objects.filter(W_All_Ded_Dept_ID=ID).values_list('Dept_ID')
        assigned_elements = HR_W_All_Ded_Department.objects.filter(W_All_Ded_Dept_ID=ID).prefetch_related("W_All_Ded_Element_ID").values("W_All_Ded_Element_ID__Element_ID", "W_All_Ded_Element_ID__Element_Name").order_by('W_All_Ded_Element_ID__Element_ID').distinct()

        if assigned_depts is None:
            return Response({'error': 'No Data Found'}, status=404)
        data = {}
        print('assigned_elements: ', assigned_elements)
        print('assigned_depts: ', assigned_depts.distinct())
        emp_list = []

        # for dept in (assigned_depts):
        #     data = assigned_emps = HR_Employees.objects.filter(Joining_Dept_ID=dept).values("Emp_ID", "Emp_Name", "")
        #     emp_list.append(data)

        # assigned_emps = HR_Employees.objects.filter(Joining_Dept_ID__in=assigned_depts).values("Emp_ID", "Emp_Name", "Joining_Dept_ID", "Joining_Dept_ID__Dept_Descr", "Joining_Dsg_ID", "Joining_Dsg_ID__DSG_Descr")
        # assigned_emps = HR_Emp_Sal_Update_Mstr.objects.filter(Dept_ID__in=assigned_depts).prefetch_related('Emp_ID', 'Dept_ID', 'Dsg_ID').values("Emp_ID", "HR_Emp_ID", "Emp_ID__Emp_Name", "Dept_ID", "Dept_ID__Dept_Descr", "Dsg_ID", "Dsg_ID__DSG_Descr")
       
        
        # Fetch records with max Emp_Up_ID per employee
        assigned_emps = HR_Emp_Sal_Update_Mstr.objects.filter(
        Dept_ID__in=assigned_depts,
        Emp_Up_ID=Subquery(max_emp_up_id_subquery)
        ).prefetch_related('Emp_ID', 'Dept_ID', 'Dsg_ID').values(
        "Emp_ID", "HR_Emp_ID", "Emp_ID__Emp_Name", "Dept_ID", "Dept_ID__Dept_Descr", "Dsg_ID", "Dsg_ID__DSG_Descr"
        )


        # assigned_emps = HR_Employees.objects.filter(Joining_Dept_ID__in=assigned_depts).values("Emp_ID", "Emp_Name", "Joining_Dept_ID", "Joining_Dept_ID__Dept_Descr", "Joining_Dsg_ID", "Joining_Dsg_ID__Dsg_Descr")
        
        print('assigned_emps: ', assigned_emps)
        # for emp in assigned_emps:
        #     print('emp: ', emp)
        #     single_emp = {
        #         'Emp_ID': emp["Emp_ID"],
        #         'Emp_Name': emp["Emp_Name"]
        #     }
        #     data.append(single_emp)
        data = {
            "Employee": assigned_emps,
            "Element": assigned_elements
        }
        print('export_template data: ', data)
        return Response(data, status=200)
    except Exception as e:
        return Response({'error': str(e)}, status=500)

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


# @api_view(['POST'])
# def Insert_Monthly_PE(request):
#     try:
#         table_data = request.data
#         print('table_data: ', table_data)

#         for item in table_data:
#             my_monthly_data = {}
#             employee_id = item.get("Employee")
#             employee_instance = HR_Employees.objects.get(pk=employee_id)
#             my_monthly_data['Employee'] = employee_instance

#             for key, value in item.items():
#                 print('Key:', key)
#                 print('Value:', value)
#                 my_monthly_data[key] = value

#             # Check if data already exists
#             existing_data = HR_Monthly_All_Ded.objects.filter(Employee=my_monthly_data['Employee'])
#             if existing_data.exists():
#                 # Update existing data
#                 existing_data.update(**my_monthly_data)
#             else:
#                 # Create new data
#                 HR_Monthly_All_Ded.objects.create(**my_monthly_data)
#     except Exception as e:
#         return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)





