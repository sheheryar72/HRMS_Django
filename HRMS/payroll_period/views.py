from django.shortcuts import render
from .models import *
from .serialiers import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from rest_framework.exceptions import NotFound

def payrollperiod_view(request):
    print('payrollperiod called')
    return render(request, 'payrollperiod.html')

@api_view(['GET'])
def get_all_finYear(request):
    try:
        queryData = HR_FinYearMstr.objects.all()
        serializerData = HR_FinYearMstrSerializer(queryData, many=True)
        return Response(serializerData.data, status=200)
    except Exception as e:
        return Response({'error': str(e)}, status=500)

@api_view(['GET'])
def get_byid_finYear(request, id):
    try:
        queryData = HR_FinYearMstr.objects.get(pk=id)
    except HR_FinYearMstr.DoesNotExist:
        return Response({'error': 'Fin year not found'}, status=status.HTTP_404_NOT_FOUND)
    serializerData = HR_FinYearMstrSerializer(queryData)
    return Response(serializerData.data, status=200)

@api_view(['POST'])
def add_finYear(request):
    print('add_finYear: ')
    print('request.data: ', request.data)
    serializer = HR_FinYearMstrSerializer(data=request.data)
    if serializer.is_valid():
        fin_year_obj = serializer.save()
        print('serializer', serializer.data)
        print('fin_year_obj.FYID: ', fin_year_obj.FYID)
        if int(request.data.get('FYStatus')) == 1:
            HR_FinYearMstr.objects.exclude(pk=fin_year_obj.FYID).update(FYStatus=False)
        print('fin_year_obj: ', fin_year_obj)
        print('fin_id: ', fin_year_obj.FYID)
        return Response({"status": "Success", "data": serializer.data}, status=201)
    else:
        return Response(serializer.errors, status=400)
    
@api_view(['PUT'])
def update_finYear(request, id):
    try:
        print('request.data.get: ', request.data.get('FYStatus'))
        if int(request.data.get('FYStatus')) == 1:
            HR_FinYearMstr.objects.exclude(pk=id).update(FYStatus=False)

        queryData = HR_FinYearMstr.objects.get(pk=id)
    except HR_FinYearMstr.DoesNotExist:
        return Response({'error': 'Financial Year not found'}, status=status.HTTP_404_NOT_FOUND)

    try:
        serializer = HR_FinYearMstrSerializer(queryData, data=request.data, partial=True)
        if serializer.is_valid():
            updated_fin_year = serializer.save()
            serialized_data = HR_FinYearMstrSerializer(updated_fin_year).data
            return Response({'message': 'Financial Year updated successfully', 'data': serialized_data}, status=status.HTTP_200_OK)

        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['DELETE'])
def delete_finYear(request, id):
    try:
        queryData = HR_FinYearMstr.objects.get(pk=id)
    except HR_FinYearMstr.DoesNotExist:
        return Response({'error': 'Fin year not found'}, status=status.HTTP_404_NOT_FOUND)

    try:
        queryData.delete()
        return Response({'message': 'Fin year deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# @api_view(['GET'])
# def get_allpayrollperiod(request, id):
#     try:
#         queryData = HR_PAYROLL_PERIOD.objects.get(pk=id)
#         payroll_month_serializer = HR_PAYROLL_MONTH_Serializer(queryData.payrollmonth)
#         finyear_serializer = HR_FinYearMstrSerializer(queryData.FinYear)
#         serializer = HR_PAYROLL_PERIOD_Serializer(queryData)
#         data = serializer.data
#         data['payrollmonth'] = payroll_month_serializer.data
#         data['FinYear'] = finyear_serializer.data
#         return Response(data, status=status.HTTP_200_OK)
#     except HR_PAYROLL_PERIOD.DoesNotExist:
#         raise NotFound(detail='Payroll period not found')
#     except Exception as e:
#         return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['GET'])
def get_allpayrollperiod(request, id):
    try:
        print('get_allpayrollperiod id: ', id)
        # queryData = HR_PAYROLL_PERIOD.objects.all
        queryData = HR_PAYROLL_PERIOD.objects.filter(FinYear__FYID=id)
        print('get_allpayrollperiod queryData: ', queryData)
        serializer = HR_PAYROLL_PERIOD_Serializer(queryData, many=True)
        print('serializer: ', serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except HR_PAYROLL_PERIOD.DoesNotExist:
        raise NotFound(detail='Payroll periods not found')
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['PUT'])
def update_month(request, id):
    try:
         # Deactivate all other payroll periods
        HR_PAYROLL_PERIOD.objects.exclude(pk=id).update(PERIOD_STATUS=False)

        queryData = HR_PAYROLL_PERIOD.objects.get(pk=id)
    except HR_PAYROLL_PERIOD.DoesNotExist:
        return Response({'error': 'Payroll Month not found'}, status=status.HTTP_404_NOT_FOUND)

    try:
        queryData.PERIOD_STATUS = True
        serializer = HR_PAYROLL_PERIOD_Serializer(queryData, data=request.data, partial=True)
        if serializer.is_valid():
            updated_instance = serializer.save()
            serialized_data = HR_PAYROLL_PERIOD_Serializer(updated_instance).data
            return Response(serialized_data, status=status.HTTP_200_OK)

        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
