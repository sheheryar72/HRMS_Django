from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import HR_W_All_Ded_Department
from .serializers import HR_W_All_Ded_Department_Serializer
from department.models import HR_Department
from payroll_element.models import HR_Payroll_Elements

# Create your views here.

def wda_view(request):
    return render(request, 'wda.html')

@api_view(['GET'])
def getall_by_wdeptid(request, wdeptid):
    try:
        print('wdeptid: ', wdeptid)
        querySet = HR_W_All_Ded_Department.objects.filter(W_All_Ded_Dept_ID=wdeptid)
        # querySet = HR_W_All_Ded_Department.objects.filter(W_All_Ded_Dept_ID=wdeptid, W_All_Ded_Element_ID_='Additional')
        # querySet = HR_W_All_Ded_Department.objects.filter(W_All_Ded_Dept_ID=wdeptid, W_All_Ded_Element_ID_='Additional').order_by('HR_Payroll_Elements__Element_Type', 'W_All_Ded_Dept_ID', 'W_All_Ded_Element_ID', 'Dept_ID')
        data = []
        for item in querySet:
            item_data = {
                'id' : item.ID,
                'W_All_Ded_ID' : item.W_All_Ded_ID,
                'W_All_Ded_Dept_ID' : item.W_All_Ded_Dept_ID.Dept_ID,
                'W_All_Ded_Element_ID' : item.W_All_Ded_Element_ID.Element_ID,
                'Dept_ID' : item.Dept_ID.Dept_ID,
                'W_All_Ded_Dept_Name': item.W_All_Ded_Dept_ID.Dept_Descr,
                'Element_Name': item.W_All_Ded_Element_ID.Element_Name,
                'Element_Type': item.W_All_Ded_Element_ID.Element_Type,
                'Element_Category': item.W_All_Ded_Element_ID.Element_Category,
                'Dept_Name': item.Dept_ID.Dept_Descr,
            }
            data.append(item_data)
        # print('getall_by_wdeptid data: ', data)
        return Response(data=data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




# @api_view(['POST'])
# def add_wda(request):
#     print('request.data: ', request.data)
#     WDAData = request.data
#     if len(WDAData) > 0:
#         unique_assignments = set()

#         distinct_w_dept_ids = set([item['W_Dept_ID'] for item in WDAData])

#         for distinct_w_dept_id in distinct_w_dept_ids:
#             max_working_id = 0
#             mode = WDAData[0].get('Mode', 0)
#             if mode == 1:
#                 HR_W_All_Ded_Department.objects.filter(W_All_Ded_Dept_ID=distinct_w_dept_id).delete()
#                 max_working_id = WDAData[0].get('W_ID', 0)
#             #else:
#                 #max_working_id = HR_W_All_Ded_Department.objects.aggregate(models.Max('W_ID'))['W_ID__max'] or 0 + 1

#             current_dept_data = [item for item in WDAData if item['W_Dept_ID'] == distinct_w_dept_id]

#             for single_data in current_dept_data:
#                 for dept_id in single_data['Departments']:
#                     for element_id in single_data['Elements']:
#                         data = HR_W_All_Ded_Department(
#                             W_All_Ded_ID=0,
#                             W_All_Ded_Dept_ID=HR_Department.objects.get(Dept_ID=distinct_w_dept_id),
#                             W_All_Ded_Element_ID=HR_Payroll_Elements.objects.get(Element_ID=element_id),
#                             Dept_ID=HR_Department.objects.get(Dept_ID=dept_id)
#                         )

#                         if data not in unique_assignments:
#                             unique_assignments.add(data)
#                             data.save()

#         return Response({'success': True})
#     else:
#         return Response({'success': False, 'message': 'No data provided'})


@api_view(['POST'])
def add_wda(request):
    print('request.data: ', request.data)
    WDAData = request.data
    if len(WDAData) > 0:
        unique_assignments = set()

        distinct_w_dept_ids = set([item['W_Dept_ID'] for item in WDAData])

        for distinct_w_dept_id in distinct_w_dept_ids:
            max_working_id = 0
            mode = WDAData[0].get('Mode', 0)
            if mode == 1:
                HR_W_All_Ded_Department.objects.filter(W_All_Ded_Dept_ID=distinct_w_dept_id).delete()
                max_working_id = WDAData[0].get('W_ID', 0)
            #else:
                #max_working_id = HR_W_All_Ded_Department.objects.aggregate(models.Max('W_ID'))['W_ID__max'] or 0 + 1

            current_dept_data = [item for item in WDAData if item['W_Dept_ID'] == distinct_w_dept_id]

            for single_data in current_dept_data:
                for dept_id in single_data['Departments']:
                    for element_id in single_data['Elements']:
                        data = HR_W_All_Ded_Department(
                            W_All_Ded_ID=0,
                            W_All_Ded_Dept_ID=HR_Department.objects.get(Dept_ID=distinct_w_dept_id),
                            W_All_Ded_Element_ID=HR_Payroll_Elements.objects.get(Element_ID=element_id),
                            Dept_ID=HR_Department.objects.get(Dept_ID=dept_id)
                        )

                        # Convert the model instance to a tuple of its attribute values
                        data_tuple = (data.W_All_Ded_ID, data.W_All_Ded_Dept_ID, data.W_All_Ded_Element_ID, data.Dept_ID)
                        
                        if data_tuple not in unique_assignments:
                            unique_assignments.add(data_tuple)
                            data.save()

        return Response({'success': True})
    else:
        return Response({'success': False, 'message': 'No data provided'})

@api_view(['POST'])
def update_wda(request, wdeptid):
    print('wdeptid: ', wdeptid)
    print('request.data: ', request.data)
    WDAData = request.data
    if len(WDAData) > 0:
        unique_assignments = set()

        distinct_w_dept_ids = set([item['W_Dept_ID'] for item in WDAData])

        for distinct_w_dept_id in distinct_w_dept_ids:
            max_working_id = 0
            mode = WDAData[0].get('Mode', 0)
            if mode == 1:
                HR_W_All_Ded_Department.objects.filter(W_All_Ded_Dept_ID=distinct_w_dept_id).delete()
                max_working_id = WDAData[0].get('W_ID', 0)

            current_dept_data = [item for item in WDAData if item['W_Dept_ID'] == distinct_w_dept_id]

            for single_data in current_dept_data:
                for dept_id in single_data['Departments']:
                    for element_id in single_data['Elements']:
                        data = HR_W_All_Ded_Department(
                            W_All_Ded_ID=0,
                            W_All_Ded_Dept_ID=HR_Department.objects.get(Dept_ID=distinct_w_dept_id),
                            W_All_Ded_Element_ID=HR_Payroll_Elements.objects.get(Element_ID=element_id),
                            Dept_ID=HR_Department.objects.get(Dept_ID=dept_id)
                        )

                        # Convert the model instance to a tuple of its attribute values
                        data_tuple = (data.W_All_Ded_ID, data.W_All_Ded_Dept_ID, data.W_All_Ded_Element_ID, data.Dept_ID)
                        
                        if data_tuple not in unique_assignments:
                            unique_assignments.add(data_tuple)
                            data.save()

        return Response({'success': True})
    else:
        return Response({'success': False, 'message': 'No data provided'})


# @api_view(['POST'])
# def add_wda(request):
#     print('request.data: ', request.data)
#     WDAData = request.data
#     # WDAData = request.data.get('WDAData', [])
#     if len(WDAData) > 0:
#         unique_assignments = set()

#         distinct_w_dept_ids = set([item['W_Dept_ID'] for item in WDAData])

#         for distinct_w_dept_id in distinct_w_dept_ids:
#             max_working_id = 0
#             mode = WDAData[0].get('Mode', 0)
#             if mode == 1:
#                 HR_W_All_Ded_Department.objects.filter(W_All_Ded_Dept_ID=distinct_w_dept_id).delete()
#                 max_working_id = WDAData[0].get('W_ID', 0)
#             #else:
#                 #max_working_id = HR_W_All_Ded_Department.objects.aggregate(models.Max('W_ID'))['W_ID__max'] or 0 + 1

#             current_dept_data = [item for item in WDAData if item['W_Dept_ID'] == distinct_w_dept_id]

#             for single_data in current_dept_data:
#                 for dept_id in single_data['Departments']:
#                     for element_id in single_data['Elements']:
#                         data = HR_W_All_Ded_Department(
#                             W_All_Ded_ID=0,
#                             W_All_Ded_Dept_ID=HR_Department.objects.get(Dept_ID=distinct_w_dept_id),
#                             W_All_Ded_Element_ID=HR_Payroll_Elements.objects.get(Element_ID=element_id),
#                             Dept_ID=HR_Department.objects.get(Dept_ID=dept_id)
#                         )

#                         if data not in unique_assignments:
#                             unique_assignments.add(data)
#                             data.save()

#         return Response({'success': True})
#     else:
#         return Response({'success': False, 'message': 'No data provided'})
    
