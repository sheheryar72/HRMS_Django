from django.shortcuts import render
from django.db import connection
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import HR_Department
from .serializers import HR_Department_Serializer
from django.http import JsonResponse
import pdb

def Department_view(request):
    print('Department called')
    return render(request, 'department.html')

@api_view(['GET'])
def get_all_department(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM HR_Department")
            departments = cursor.fetchall()

        #pdb.set_trace()

        Department_objects = [HR_Department(Dept_ID=department[0], Dept_Descr=department[1]) for department in departments]
        serializer = HR_Department_Serializer(Department_objects, many=True)
        
        # print('departments query: ', departments)
        # print('departments model: ', Department_objects)
        # print('departments serializer: ', serializer)
        # print('departments json: ', serializer.data)

        #return Response(serializer.data)
        return JsonResponse(serializer.data, safe=False)


    except Exception as e:
        return Response({'error': str(e)}, status=500)

@api_view(['GET'])
def get_department_by_id(request, department_id):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM HR_Department WHERE Dept_ID = %s", [department_id])
            department = cursor.fetchone()
            #Department = HR_Department.objects.get(pk=Department_id)

        if department:
            Department_object = HR_Department(Dept_ID=department[0], Dept_Descr=department[1])
            serializer = HR_Department_Serializer(Department_object)
            return Response(serializer.data)

        return Response({'error': 'Department not found'}, status=404)

    except Exception as e:
        return Response({'error': str(e)}, status=500)

@api_view(['POST'])
def insert_department(request):
    try:
        serializer = HR_Department_Serializer(data=request.data)
        if serializer.is_valid():
            new_Department = serializer.save()
            serialized_data = HR_Department_Serializer(new_Department).data
            return Response(serialized_data, status=status.HTTP_201_CREATED)

        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['PUT'])
def update_department(request, department_id):
    try:
        department = HR_Department.objects.get(pk=department_id)
    except HR_Department.DoesNotExist:
        return Response({'error': 'Department not found'}, status=status.HTTP_404_NOT_FOUND)

    try:
        serializer = HR_Department_Serializer(department, data=request.data, partial=True)
        if serializer.is_valid():
            updated_Department = serializer.save()
            serialized_data = HR_Department_Serializer(updated_Department).data
            return Response(serialized_data, status=status.HTTP_200_OK)

        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['DELETE'])
def delete_department(request, department_id):
    try:
        Department = HR_Department.objects.get(pk=department_id)
    except HR_Department.DoesNotExist:
        return Response({'error': 'Department not found'}, status=status.HTTP_404_NOT_FOUND)

    try:
        Department.delete()
        return Response({'message': 'Department deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

