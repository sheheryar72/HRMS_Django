from django.shortcuts import render
from .models import *
from .serialiers import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from rest_framework.exceptions import NotFound
from django.db.models import Max, Min, Count
from django.core.exceptions import ObjectDoesNotExist 
from django.views.decorators.csrf import csrf_exempt

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

# @api_view(['POST'])
# def add_finYear(request):
#     print('add_finYear: ')
#     print('request.data: ', request.data)
#     serializer = HR_FinYearMstrSerializer(data=request.data)
#     if serializer.is_valid():
#         fin_year_obj = serializer.save()
#         print('serializer', serializer.data)
#         print('fin_year_obj.FYID: ', fin_year_obj.FYID)
#         if int(request.data.get('FYStatus')) == 1:
#             HR_FinYearMstr.objects.exclude(pk=fin_year_obj.FYID).update(FYStatus=False)
#         print('fin_year_obj: ', fin_year_obj)
#         print('fin_id: ', fin_year_obj.FYID)    
#         payroll_period_data = add_payroll_period(fin_year_obj.FYID)
#         print("payroll_period_data: ", payroll_period_data)
#         # HR_PAYROLL_PERIOD.objects.bulk_create(payroll_period_data)
#         return Response({"status": "Success", "data": serializer.data}, status=201)
#     else:
#         return Response(serializer.errors, status=400)
    
# def add_payroll_period(finid):
#     max_pp = HR_PAYROLL_PERIOD.objects.aggregate(max("Period_ID"))
#     payroll_period = []
#     max_pp += 1
#     for i in range(12):
#        i += 1
#        data = {
#         "Period_ID": max_pp,
#         "FYID": finid,
#         "MNTH_ID": i,
#         "Period_STATUS": 0,
#         }
#        payroll_period.append(data)
#     return payroll_period

@csrf_exempt
@api_view(['POST'])
def add_finYear(request):
    try:
        serializer = HR_FinYearMstrSerializer(data=request.data)    
        if serializer.is_valid():
            fin_year_obj = serializer.save()
            if int(request.data.get('FYStatus')) == 1:
                HR_FinYearMstr.objects.exclude(FYID=fin_year_obj.FYID).update(FYStatus=False)
            payroll_period_data = add_payroll_period(fin_year_obj.FYID, fin_year_obj.FinYear)
            print("payroll_period_data payroll_period_data: ", payroll_period_data)
            pp_serializer = HR_PAYROLL_PERIOD_Serializer(data=payroll_period_data, many=True)
            if pp_serializer.is_valid():
                pp_serializer.save()
            else:
                return Response(pp_serializer.errors, status=400)
            return Response({"status": "Success", "data": serializer.data}, status=201)
        else:
            return Response(serializer.errors, status=400)
    except Exception as e:
        return Response({"error": str(e)}, status=500)

def add_payroll_period(finid, FinYear):
    max_pp = HR_PAYROLL_PERIOD.objects.aggregate(max_id=Max("PERIOD_ID"))['max_id'] or 0
    payroll_period = []
    max_pp += 1
    finyears = FinYear.split('-')
    for i in range(1, 13):
        data = {
            "ID": 0,
            "PERIOD_ID": max_pp,
            "FYID": finid,
            "MNTH_ID": i,
            "PERIOD_STATUS": 0,
            "PERIOD_YEAR": finyears[0] if i <= 7 else finyears[1]
        }
        payroll_period.append(data)
    return payroll_period

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


@api_view(['GET'])
def get_payroll_status_byid(request, payroll_id, filename):
    try:
        queryData = HR_PAYROLL_PERIOD.objects.filter(PAYROLL_ID=payroll_id).first()
        if queryData.PAYROLL_FINAL == filename:
            return queryData.PAYROLL_FINAL
        if queryData.PAYSHEET_FINAL == filename:
            return queryData.PAYSHEET_FINAL
    except HR_FinYearMstr.DoesNotExist:
        return Response({'error': 'payrollsheet not found'}, status=status.HTTP_404_NOT_FOUND)
    serializerData = HR_FinYearMstrSerializer(queryData)
    return Response(serializerData.data, status=200)


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
    
# @api_view(['GET'])
# def get_allpayrollperiod(request, id):
#     try:
#         # Fetch payroll periods with the specified FYID
#         queryData = HR_PAYROLL_PERIOD.objects.filter(FYID=id).select_related('FYID', 'MNTH_ID')
#         # Create a list of dictionaries containing payroll period data
#         data_list = []
#         for item in queryData:
#             single_data = {
#                 'ID': item.ID,
#                 'PERIOD_ID': item.PERIOD_ID,
#                 'FYID': item.FYID.FYID,
#                 'FinYear': item.FYID.FinYear,
#                 'MNTH_ID': item.MNTH_ID.MNTH_ID,
#                 'MNTH_NO': item.MNTH_ID.MNTH_NO,
#                 'MNTH_NAME': item.MNTH_ID.MNTH_NAME,
#                 'MNTH_SHORT_NAME': item.MNTH_ID.MNTH_SHORT_NAME,
#                 'PERIOD_STATUS': item.PERIOD_STATUS
#             }
#             data_list.append(single_data)


#         print('data_list: ', data_list)
#         return Response(data=data_list, status=status.HTTP_200_OK)
#     except ObjectDoesNotExist:
#         raise NotFound(detail='Payroll periods not found')
#     except Exception as e:
#         return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['GET'])
def get_allpayrollperiod(request, id):
    try:
        print('id:  ', id)
        print('get_allpayrollperiod get_allpayrollperiod')
        queryData = HR_PAYROLL_PERIOD.objects.filter(FYID=id).select_related('FYID', 'MNTH_ID')
        
        print("get_allpayrollperiod: queryData: ", queryData)

        data_list = []

        for item in queryData:
            single_pp = {
                'ID': item.PAYROLL_ID,
                'FYID': item.FYID.FYID,
                'FinYear': item.FYID.FinYear,
                'PERIOD_ID': item.PERIOD_ID,
                'PERIOD_STATUS': item.PERIOD_STATUS,
                'MNTH_ID': item.MNTH_ID.MNTH_ID,
                'MNTH_NO': item.MNTH_ID.MNTH_NO,
                'MNTH_NAME': item.MNTH_ID.MNTH_NAME,
                'MNTH_SHORT_NAME': item.MNTH_ID.MNTH_SHORT_NAME,
                'PAYROLL_FINAL': item.PAYROLL_FINAL,
                'PAYSHEET_FINAL': item.PAYSHEET_FINAL
            }
            data_list.append(single_pp)

        # data_list = HR_PAYROLL_PERIOD_Serializer(queryData, many=True)

        return Response(data=data_list, status=status.HTTP_200_OK)
    except ObjectDoesNotExist:
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


# @api_view(['PUT'])
# def update_payroll_final_status(request, id, payroll_type, payroll_status):
#     # try:
#     #      # Deactivate all other payroll periods
#     #     if payroll_type == 'paysheet':
#     #         HR_PAYROLL_PERIOD.objects.get(pk=id).update(PAYSHEET_FINAL=payroll_status)
#     #     elif payroll_type == 'process':
#     #         HR_PAYROLL_PERIOD.objects.get(pk=id).update(PAYROLL_FINAL=payroll_status)

#     #     queryData = HR_PAYROLL_PERIOD.objects.get(pk=id)
#     #     queryData.
#     # except HR_PAYROLL_PERIOD.DoesNotExist:
#     #     return Response({'error': 'Payroll Month not found'}, status=status.HTTP_404_NOT_FOUND)


#     try:
#         queryData = HR_PAYROLL_PERIOD.objects.get(pk=id)
#         print('queryData: ', queryData.__dict__)
#         print('payroll_type: ', payroll_type)
#         if payroll_type == 'paysheet':
#             print('if paysheet')
#             queryData.PAYSHEET_FINAL = True
#         elif payroll_type == 'process':
#             print('if process')
#             queryData.PAYROLL_FINAL = True

#         queryData.save()
#         serializer = HR_PAYROLL_PERIOD_Serializer(queryData)
#         if serializer.is_valid():
#         #     updated_instance = serializer.save()
#         #     serialized_data = HR_PAYROLL_PERIOD_Serializer(updated_instance).data
#             return Response(serializer, status=status.HTTP_200_OK)

#         return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

#     except Exception as e:
#         return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PUT'])
def update_payroll_final_status(request, id, payroll_type, payroll_status):
    try:
        # Convert payroll_status to a boolean if it's 1 or 0
        if isinstance(payroll_status, int):
            payroll_status = bool(payroll_status)
        elif isinstance(payroll_status, str):
            payroll_status = payroll_status.lower() == 'true'
        else:
            return Response({'error': 'Invalid payroll_status value'}, status=status.HTTP_400_BAD_REQUEST)

        # Fetch the HR_PAYROLL_PERIOD instance
        try:
            queryData = HR_PAYROLL_PERIOD.objects.get(pk=id)
        except HR_PAYROLL_PERIOD.DoesNotExist:
            return Response({'error': 'Payroll Month not found'}, status=status.HTTP_404_NOT_FOUND)

        # Update based on payroll_type
        if payroll_type == 'paysheet':
            queryData.PAYSHEET_FINAL = payroll_status
        elif payroll_type == 'process':
            queryData.PAYROLL_FINAL = payroll_status
        else:
            return Response({'error': 'Invalid payroll_type'}, status=status.HTTP_400_BAD_REQUEST)

        # Save the updated instance
        queryData.save()

        # Serialize and return the updated instance
        serializer = HR_PAYROLL_PERIOD_Serializer(queryData)
        return Response(serializer.data, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({'error': f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


