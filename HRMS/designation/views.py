from django.shortcuts import render
from django.db import connection
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import HR_Designation
from .serializers import HR_Designation_Serializer

def Designation_view(request):
    print('Designation called')
    return render(request, 'designation.html')

@api_view(['GET'])
def get_all_designation(request):
    try:
        designation = HR_Designation.getall_designation()
        serializer = HR_Designation_Serializer(designation, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({'error': str(e)}, status=500)

@api_view(['GET'])
def get_designation_by_id(request, designation_id):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM HR_Designation WHERE DSG_ID = %s", [designation_id])
            designation = cursor.fetchone()
            #Designation = HR_Designation.objects.get(pk=Designation_id)

        if designation:
            designation_object = HR_Designation(DSG_ID=designation[0], DSG_Descr=designation[1])
            serializer = HR_Designation_Serializer(designation_object)
            return Response(serializer.data)

        return Response({'error': 'Designation not found'}, status=404)

    except Exception as e:
        return Response({'error': str(e)}, status=500)


@api_view(['POST'])
def insert_designation(request):
    try:
        serializer = HR_Designation_Serializer(data=request.data)
        if serializer.is_valid():
            new_Designation = serializer.save()
            serialized_data = HR_Designation_Serializer(new_Designation).data
            return Response(serialized_data, status=status.HTTP_201_CREATED)

        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PUT'])
def update_designation(request, designation_id):
    try:
        Designation = HR_Designation.objects.get(pk=designation_id)
    except HR_Designation.DoesNotExist:
        return Response({'error': 'Designation not found'}, status=status.HTTP_404_NOT_FOUND)

    try:
        serializer = HR_Designation_Serializer(Designation, data=request.data, partial=True)
        if serializer.is_valid():
            updated_Designation = serializer.save()
            serialized_data = HR_Designation_Serializer(updated_Designation).data
            return Response(serialized_data, status=status.HTTP_200_OK)

        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['DELETE'])
def delete_designation(request, designation_id):
    try:
        Designation = HR_Designation.objects.get(pk=designation_id)
    except HR_Designation.DoesNotExist:
        return Response({'error': 'Designation not found'}, status=status.HTTP_404_NOT_FOUND)

    try:
        Designation.delete()
        return Response({'message': 'Designation deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

