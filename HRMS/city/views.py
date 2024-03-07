from django.shortcuts import render
from django.db import connection
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import HR_City
from .serializers import HR_CITY_Serializer

def city_view(request):
    print('city called')
    return render(request, 'city.html')

# @api_view(['GET'])
# def get_all_cities(request):
#     try:
#         with connection.cursor() as cursor:
#             cursor.execute("SELECT * FROM HR_CITY")
#             cities = cursor.fetchall()

#         city_objects = [HR_City(CT_ID=city[0], CT_Descr=city[1]) for city in cities]
#         serializer = HR_CITY_Serializer(city_objects, many=True)
#         return Response(serializer.data)

#     except Exception as e:
#         return Response({'error': str(e)}, status=500)

@api_view(['GET'])
def get_all_cities(request):
    try:
        cities = HR_City.objects.all()
        print('cities: ', cities)
        print('cities.count(): ', cities.count())

        #city_objects = [HR_City(CT_ID=city.CT_ID, CT_Descr=city.CT_Descr) for city in cities]
        #serializer = HR_CITY_Serializer(city_objects, many=True)
        serializer = HR_CITY_Serializer(cities, many=True)
        return Response(serializer.data)

    except Exception as e:
        return Response({'error': str(e)}, status=500)

@api_view(['GET'])
def get_city_by_id(request, city_id):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM HR_CITY WHERE CT_ID = %s", [city_id])
            city = cursor.fetchone()
            #city = HR_City.objects.get(pk=city_id)

        if city:
            city_object = HR_City(CT_ID=city[0], CT_Descr=city[1])
            serializer = HR_CITY_Serializer(city_object)
            return Response(serializer.data)

        return Response({'error': 'City not found'}, status=404)

    except Exception as e:
        return Response({'error': str(e)}, status=500)

@api_view(['POST'])
def insert_city(request):
    try:
        serializer = HR_CITY_Serializer(data=request.data)
        if serializer.is_valid():
            new_city = serializer.save()
            serialized_data = HR_CITY_Serializer(new_city).data
            return Response(serialized_data, status=status.HTTP_201_CREATED)

        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['PUT'])
def update_city(request, city_id):
    try:
        city = HR_City.objects.get(pk=city_id)
    except HR_City.DoesNotExist:
        return Response({'error': 'City not found'}, status=status.HTTP_404_NOT_FOUND)

    try:
        serializer = HR_CITY_Serializer(city, data=request.data, partial=True)
        if serializer.is_valid():
            updated_city = serializer.save()
            serialized_data = HR_CITY_Serializer(updated_city).data
            return Response(serialized_data, status=status.HTTP_200_OK)

        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['DELETE'])
def delete_city(request, city_id):
    try:
        city = HR_City.objects.get(pk=city_id)
    except HR_City.DoesNotExist:
        return Response({'error': 'City not found'}, status=status.HTTP_404_NOT_FOUND)

    try:
        city.delete()
        return Response({'message': 'City deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

