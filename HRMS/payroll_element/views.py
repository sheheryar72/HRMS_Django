from django.shortcuts import render
from .models import HR_Payroll_Elements, HR_Payroll_Elements_Serializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db import connection

def payrollelement(request):
    return render(request, 'payrollelement.html')

@api_view(['GET'])
def getall(request):
    try:
        payrollelements = HR_Payroll_Elements.objects.all()
        serializer = HR_Payroll_Elements_Serializer(payrollelements, many=True)
        return Response(serializer.data, status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def getbyid(request, id):
    try:
        try:
            payrollelement = HR_Payroll_Elements.objects.get(pk=id)
        except Exception as e:
            return Response({'no data found': str(e)}, status.HTTP_404_NOT_FOUND)
        serializer = HR_Payroll_Elements_Serializer(payrollelement)
        return Response(serializer.data, status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['DELETE'])
def delete(request, id):
    try:
        try:
            payrollelement = HR_Payroll_Elements.objects.get(pk=id)
            payrollelement.delete()
        except Exception as e:
            return Response({'no data found': str(e)}, status.HTTP_404_NOT_FOUND)
        return Response("Data Deleted Successfully", status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def add_payrollelement(request):
    try:
        data = request.data
        print('add_payrollelement: received data: ', data)
        
        element_name = data.get('Element_Name')
        element_type = data.get('Element_Type')
        element_category = data.get('Element_Category')
        cal_type = data.get('Cal_Type')

        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO HR_Payroll_Elements (Element_Name, Element_Type, Element_Category, Cal_Type)
                VALUES (%s, %s, %s, %s)
            """, [element_name, element_type, element_category, cal_type])

        return Response(data, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        print('add_payrollelement: exception occurred', str(e))
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['PUT'])
def update_payrollelement(request, id):
    try:
        try:
            payrollelement = HR_Payroll_Elements.objects.get(pk=id)
        except Exception as e:
            return Response({'error': str(e)}, status.HTTP_404_NOT_FOUND)
        data = request.data
        serializer = HR_Payroll_Elements_Serializer(payrollelement, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return  Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status.HTTP_500_INTERNAL_SERVER_ERROR)
        



