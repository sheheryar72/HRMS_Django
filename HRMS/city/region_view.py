from django.shortcuts import render
from django.db import connection
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import HR_Region
from .serializers import HR_Region_Serializer

def region_view(request):
    print('region called')
    return render(request, 'region.html')

@api_view(['GET'])
def get_all_regions(request):
    try:
        regions = HR_Region.objects.all()
        print('regions: ', regions)
        print('regions uguuggug(): ', regions.count())

        serializer = HR_Region_Serializer(regions, many=True)
        return Response(serializer.data)

    except Exception as e:
        return Response({'error': str(e)}, status=500)

@api_view(['GET'])
def get_region_by_id(request, region_id):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM HR_Region WHERE CT_ID = %s", [region_id])
            region = cursor.fetchone()

        if region:
            region_object = HR_Region(CT_ID=region[0], CT_Descr=region[1])
            serializer = HR_Region_Serializer(region_object)
            return Response(serializer.data)

        return Response({'error': 'region not found'}, status=404)

    except Exception as e:
        return Response({'error': str(e)}, status=500)

@api_view(['POST'])
def insert_region(request):
    try:
        serializer = HR_Region_Serializer(data=request.data)
        if serializer.is_valid():
            new_region = serializer.save()
            serialized_data = HR_Region_Serializer(new_region).data
            return Response(serialized_data, status=status.HTTP_201_CREATED)

        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PUT'])
def update_region(request, region_id):
    try:
        region = HR_Region.objects.get(pk=region_id)
    except HR_Region.DoesNotExist:
        return Response({'error': 'region not found'}, status=status.HTTP_404_NOT_FOUND)

    try:
        serializer = HR_Region_Serializer(region, data=request.data, partial=True)
        if serializer.is_valid():
            updated_region = serializer.save()
            serialized_data = HR_Region_Serializer(updated_region).data
            return Response(serialized_data, status=status.HTTP_200_OK)

        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['DELETE'])
def delete_region(request, region_id):
    try:
        region = HR_Region.objects.get(pk=region_id)
    except HR_Region.DoesNotExist:
        return Response({'error': 'region not found'}, status=status.HTTP_404_NOT_FOUND)

    try:
        region.delete()
        return Response({'message': 'region deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

