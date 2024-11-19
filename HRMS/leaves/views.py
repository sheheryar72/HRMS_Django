from django.shortcuts import render
from .models import HR_Leaves
from .serializers import HR_Leaves_Serializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from payroll_period.models import HR_FinYearMstr
from employee.models import HR_Employees

# def leaves(request):
#     return render(request, 'leaves.html')

def leaves_view(request):
    print('leaves_view called')
    return render(request, 'leaves.html')

@api_view(['GET'])
def getall(request):
    try:
        leavess = HR_Leaves.objects.all().select_related('FYID', 'Emp_ID')
        # serializer = HR_Leaves_Serializer(leavess, many=True)
        data = []
        for item in leavess:
            leaves_data = {
                'Leaves_ID': item.Leaves_ID,
                'FYID': item.FYID.FYID,
                'FinYear': item.FYID.FinYear,
                'Emp_ID': item.Emp_ID.Emp_ID,
                'Joining_Date': item.Emp_ID.Joining_Date,
                'Emp_Name': item.Emp_ID.Emp_Name,
                'HR_Emp_ID': item.Emp_ID.HR_Emp_ID,
                'EL_OP': item.EL_OP,
                'CL': item.CL,
                'SL': item.SL,
                'EL': item.EL,
                'LA_EL': item.LA_EL,
                'EGL': item.EGL,
                'LA_CL': item.LA_CL,
                'LA_SL': item.LA_SL,
                'LA_EGL': item.LA_EGL,
                'LA_EL_OP': item.LA_EL_OP,
                'Tot_LA': item.Tot_LA
            }
            data.append(leaves_data)

        return Response(data, status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def getbyid(request, id):
    try:
        try:
            item = HR_Leaves.objects.get(pk=id)
            leaves_data = {
                'Leaves_ID': item.Leaves_ID,
                'FYID': item.FYID.FYID,
                'FinYear': item.FYID.FinYear,
                'Emp_ID': item.Emp_ID.Emp_ID,
                'Joining_Date': item.Emp_ID.Joining_Date,
                'Emp_Name': item.Emp_ID.Emp_Name,
                'HR_Emp_ID': item.Emp_ID.HR_Emp_ID,
                'EL_OP': item.EL_OP,
                'CL': item.CL,
                'SL': item.SL,
                'EL': item.EL,
                'LA_EL': item.LA_EL,
                'EGL': item.EGL,
                'LA_CL': item.LA_CL,
                'LA_SL': item.LA_SL,
                'LA_EGL': item.LA_EGL,
                'LA_EL_OP': item.LA_EL_OP,
                'Tot_LA': item.Tot_LA
            }
        except Exception as e:
            return Response({'no data found': str(e)}, status.HTTP_404_NOT_FOUND)
        # serializer = HR_Leaves_Serializer(leaves)
        return Response(leaves_data, status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['DELETE'])
def delete(request, id):
    try:
        try:
            leaves = HR_Leaves.objects.get(pk=id)
            leaves.delete()
        except Exception as e:
            return Response({'no data found': str(e)}, status.HTTP_404_NOT_FOUND)
        return Response("Data Deleted Successfully", status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def add_leaves(request):
    try:
        data = request.data

        # finyear_data = HR_FinYearMstr.objects.get(pk=request.data.get('FYID'))
        # emp_data = HR_Employees.objects.get(pk=request.data.get('Emp_ID'))
        # data['FYID'] = finyear_data
        # HR_Leaves.objects.create(FYID=finyear_data, Emp_ID=emp_data, EL_OP=request.data.get('EL_OP'), CL=request.data.get('CL'), 
        #                          SL=request.data.get('SL'), EL=request.data.get('EL'))
        print('add_leaves')
        print('request.data: ', request.data)
        serializer = HR_Leaves_Serializer(data=data)
        print('serializer')
        if serializer.is_valid():
            print('saveeee')
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
        
        return Response("User created successfully", status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'error': str(e)}, status.HTTP_500_INTERNAL_SERVER_ERROR)
        
@api_view(['PUT'])
def update_leaves(request, id):
    try:
        try:
            leaves = HR_Leaves.objects.get(pk=id)
        except Exception as e:
            return Response({'error': str(e)}, status.HTTP_404_NOT_FOUND)
        data = request.data
        serializer = HR_Leaves_Serializer(leaves, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return  Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status.HTTP_500_INTERNAL_SERVER_ERROR)
        



