from django.shortcuts import render
from rest_framework.generics import ListAPIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import HR_Emp_Sal_Update_Mstr, HR_Emp_Sal_Update_Dtl
from .serializer import HR_Emp_Sal_Update_Dtl_Serializer, HR_Emp_Sal_Update_Mstr_Serializer
from employee.models import HR_Employees
from employee.serializers import HR_Employees_Serializer
from django.db.models import Subquery
from rest_framework import status
from payroll_element.models import HR_Payroll_Elements, HR_Payroll_Elements_Serializer
import pdb

def salaryupdate_view(request):
    return render(request, 'salaryupdate.html')

@api_view(['GET'])  
def getall_salaryupdate(request):
    try:
        emp_ids = HR_Emp_Sal_Update_Mstr.objects.values('Emp_ID')
        queryset_emp_salaryupdate = HR_Employees.objects.exclude(Emp_ID__in=Subquery(emp_ids)).all()    
        serializer = HR_Employees_Serializer(queryset_emp_salaryupdate, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])  
def getll_emp_notin_salaryupdate(request):
    try:
        emp_ids = HR_Emp_Sal_Update_Mstr.objects.values('Emp_ID')
        queryset_emp_salaryupdate = HR_Employees.objects.exclude(Emp_ID__in=Subquery(emp_ids)).all()
        serializer = HR_Employees_Serializer(queryset_emp_salaryupdate, many=True)
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
            master_serializer = HR_Emp_Sal_Update_Mstr_Serializer(data=request.data.get("masterData", {}))
            if master_serializer.is_valid():
                master_serializer.save()
                print("master saved")
                print("master_serializer: ", master_serializer.data)
                print("master_serializer.data.Emp_Up_ID: ", master_serializer.data['Emp_Up_ID'])
                detailList = request.data.get('detailList', [])
                for detail_data in detailList:
                    detail_data['Emp_Up_ID'] = master_serializer.data['Emp_Up_ID']
                    detail_data['Emp_ID'] = master_serializer.data['Emp_ID']
                    detail_serializer = HR_Emp_Sal_Update_Dtl_Serializer(data=detail_data)
                    if detail_serializer.is_valid():
                        detail_serializer.save()
                        print("detail saved")
                    else:
                        return Response(detail_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response(master_serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def update_salary_update(request, empupid):
        try:
            print("update salary")
            print("empupid: ", empupid)
            print("masterData data: ", request.data.get("masterData", {}))
            print("detailList data: ", request.data.get('detailList', []))
            master_querysery = HR_Emp_Sal_Update_Mstr.objects.get(pk=empupid)
            detail_queryset = HR_Emp_Sal_Update_Mstr.objects.get(Emp_Up_ID=empupid)
            if master_querysery is None:
                Response({'error': 'no salary found'}, status=status.HTTP_404_NOT_FOUND)
            
            if master_querysery and detail_queryset is not None:
                HR_Emp_Sal_Update_Mstr.objects.filter(Emp_Up_ID=empupid).delete()
                HR_Emp_Sal_Update_Dtl.objects.filter(Emp_Up_ID=empupid).delete()

            master_serializer = HR_Emp_Sal_Update_Mstr_Serializer(data=request.data.get("masterData", {}))
            # master_serializer = HR_Emp_Sal_Update_Mstr_Serializer(master_querysery, data=request.data.get("masterData", {}), partial=True)
            if master_serializer.is_valid():
                master_serializer.save()
                print("master updated")
                print("master_serializer: ", master_serializer.data)
                print("master_serializer.data.Emp_Up_ID: ", master_serializer.data['Emp_Up_ID'])
                detailList = request.data.get('detailList', [])

                for detail_data in detailList:
                    detail_data['Emp_Up_ID'] = master_serializer.data['Emp_Up_ID']
                    detail_data['Emp_ID'] = master_serializer.data['Emp_ID']
        
                    # detail_queryset = HR_Emp_Sal_Update_Dtl.objects.get(Emp_ID=empupid)

                    detail_serializer = HR_Emp_Sal_Update_Dtl_Serializer(data=detail_data)
                    if detail_serializer.is_valid():
                        detail_serializer.save()
                        print("detail updated")
                    else:
                        return Response(detail_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response(master_serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['PUT'])
def update_salary_Update(request, pk):
    try:
        master_instance = HR_Emp_Sal_Update_Mstr.objects.get(pk=pk)
        master_serializer = HR_Emp_Sal_Update_Mstr_Serializer(instance=master_instance, data=request.data.get('masterData', {}))
        if not master_serializer.is_valid():
            return Response(master_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        master_serializer.save()

        detail_querySet_list = HR_Emp_Sal_Update_Dtl.objects.filter(Emp_Up_ID=pk)
        for detail_querySet in detail_querySet_list:
            detail_request = next((item for item in request.data.get("detailList", []) if item['id'] == detail_querySet.id), None)
            if detail_request:
                detail_serializer = HR_Emp_Sal_Update_Dtl_Serializer(instance=detail_querySet, data=detail_request)
                if detail_serializer.is_valid():
                    detail_serializer.save()
                else:
                    return Response(detail_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message": "Salary update updated successfully"}, status=status.HTTP_200_OK)
    except HR_Emp_Sal_Update_Mstr.DoesNotExist:
        return Response({'error': 'Master record not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def getall_payroll_element_notin_su(request, empUpID, empID):
    try:
        print('empID: ', empID)
        print('empUpID: ', empUpID)
        if empID is None or empUpID is None:
            return Response({'error': 'Salary not found'}, status=status.HTTP_404_NOT_FOUND)
        su_queryset = HR_Emp_Sal_Update_Dtl.objects.filter(Emp_ID=empID, Emp_Up_ID=empUpID).values_list("Element_ID", flat=True)
        element_queryset = HR_Payroll_Elements.objects.exclude(Element_ID__in=su_queryset)
        serializer = HR_Payroll_Elements_Serializer(element_queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def getall_master_byid(request, empUpID, empID):
    try:
        if not empID or not empUpID:
            return Response({'error': 'Employee ID or Update ID not provided'}, status=status.HTTP_400_BAD_REQUEST)
        print("up is: ", empUpID)
        print("empID: ", empID)
        # detail_queryset = HR_Emp_Sal_Update_Dtl.objects.filter(Emp_Up_ID=empUpID)
        # detail_queryset = HR_Emp_Sal_Update_Dtl.objects.filter(Emp_Up_ID=empUpID, Emp_ID=empID).select_related('Emp_Up_ID', 'Emp_ID', 'Element_ID')
        detail_queryset = HR_Emp_Sal_Update_Dtl.objects.filter(Emp_Up_ID=empUpID, Emp_ID=empID)
        datas = []
        print('detail_queryset: ', detail_queryset)
        for data in detail_queryset:
            print('data: ', data)
            item = {
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
                "No_of_Children": data.Emp_Up_ID.No_of_Children
            }
            datas.append(item)
        print("DAtas: ", datas)
        return Response(datas, status=status.HTTP_200_OK)
    except HR_Emp_Sal_Update_Dtl.DoesNotExist:
        return Response({'error': 'Salary not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# @api_view(['GET'])
# def getall_master_byid(request, empID, empUpID):
#     try:
#         print('empID: ', empID)
#         print('empUpID: ', empUpID)
#         if empID is None or empUpID is None:
#             return Response({'error': 'Salary not found'}, status=status.HTTP_404_NOT_FOUND) 
#         detail_queryset = HR_Emp_Sal_Update_Dtl.objects.filter(Emp_Up_ID=empUpID, Emp_ID=empID)
#         print("detail_queryset: ", detail_queryset)
#         datas = []
#         for data in detail_queryset:
#             item = {
#             "Emp_Up_ID": data.Emp_Up_ID.Emp_Up_ID,
#             "Emp_Up_Date": data.Emp_Up_ID.Emp_Up_Date,
#             "Emp_ID": data.Emp_ID.Emp_ID,
#             "Emp_Name": data.Emp_ID.Emp_Name,
#             "HR_Emp_ID": data.Emp_ID.HR_Emp_ID,
#             "Emp_Category": data.Emp_Up_ID.Emp_Category,
#             "GrossSalary": data.Emp_Up_ID.GrossSalary,  
#             "Amount": data.Amount,
#             "Element_Category": data.Element_Category,
#             "Element_ID": data.Element_ID.Element_ID,
#             "Element_Name": data.Element_ID.Element_Name,
#             "Element_Type": data.Element_Type,
#             "Remarks": data.Emp_Up_ID.Remarks,
#             # "Dsg_ID": data.Emp_Up_ID.Dsg_ID,
#             # "DSG_Descr": data.Emp_Up_ID.Dept_ID.Dept_Descr,
#             "Grade_ID": data.Emp_Up_ID.Grade_ID,
#             "Grade.Grade_Descr": data.Emp_Up_ID.Grade_ID.Grade_Descr,
#             "Co_ID": data.Emp_ID.Co_ID,
#             "Dept_ID": data.Emp_Up_ID.Dept_ID,
#             "Department.Dept_Descr": data.Emp_Up_ID.Dept_ID.Dept_Descr,
#             "Marital_Status": data.Emp_ID.Marital_Status,
#             "No_of_Children": data.Emp_Up_ID.No_of_Children
#             }
#             datas.append(item)
#         return Response(datas, status=status.HTTP_200_OK)
#     except Exception as e:
#         return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def getll_master(request):
    try:
        querySet = HR_Emp_Sal_Update_Mstr.objects.all()
        print('querySet: ', querySet.count())
        datas = []
        for item in querySet:
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
        print('datas: ', datas)
        return Response(datas, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

