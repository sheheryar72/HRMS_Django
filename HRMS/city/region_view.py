from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework.response import Response

def region_view(request):
    return render(request, 'region.html')

def getall(request):
    try:
        regions = HR_Region.objects.all()
        regions_serializer = HR_Region_Serializer(regions, many=True)
        return Response(regions_serializer.data, status=200)
    except Exception as e:
        return Response({'error': str(e)}, status=500)

def getby_ID(request, id):
    try:
        region = HR_Region.objects.get(pk=id)
        region_serializer = HR_Region_Serializer(region)
        return Response(region_serializer.data, status=200)
    except Exception as e:
        return Response({'error': str(e)}, status=500)

def add(request):
    try:
        data = request.data.get('region_data', [])
        region_serializer = HR_Region_Serializer(data=data)
        if region_serializer.is_valid():
            region_serializer.save()
            return Response(region_serializer.data, status=201)
        else:
            return Response({'error': str(region_serializer.errors)}, status=400)
    except Exception as e:
        return Response({'error': str(e)}, status=500)

def update(request, id):
    try:
        data = request.data.get('request_data', [])
        region_data = HR_Region.objects.get(pk=id)
        if region_data is None:
            return Response({'error': 'Region not found'}, status=404)
        region_serializer = HR_Region_Serializer(region_data, data=data)
        if region_serializer.is_valid():
            region_serializer.save()
            return Response(region_serializer.data, status=200)
        return Response({'error': str(e)}, status=400)
    except Exception as e:
        return Response({'error': str(e)}, status=500)

def delete(request, id):
    try:
        region_data = HR_Region.objects.get(pk=id)
        if region_data is None:
            return Response({'error': 'Region not found'}, status=404)
        HR_Region.objects.filter(pk=id).delete()    
        return Response({'error'})
    except Exception as e:
        return Response({'error': str(e)}, status=500)



