from django.shortcuts import render
from .models import User_Froms, GroupOfCompanies, FormDescription
from hr_login.models import UserLogin
from .serializers import User_Froms_Serializer, GroupOfCompanies_Serializer, FormDescription_Serializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from hr_login.serializers import User_Login_Serializer
from django.db.models import Sum, Count, Avg, Min, Max

def view_userprivileges(request):
    return render(request, template_name='userprivileges.html')

@api_view(['GET'])
def getall_userprivileges(request, userid):
    try:
        print('userid: ',userid)
        # userforms = User_Froms.objects.filter(UserDetail__User_ID=userid)
        userforms = User_Froms.objects.filter(UserDetail__User_ID=userid, COID=1)
        print('userforms: ',userforms)
        serializer = User_Froms_Serializer(userforms, many=True)
        print('serializer: ',serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def getall_groupofcompanies(request):
    try:
        groupofcompanies = GroupOfCompanies.objects.all()
        serializer = GroupOfCompanies_Serializer(groupofcompanies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def add_userprivileges(request):
    try:
        insertedUser = UserLogin.objects.create(
            User_Emp_Code=request.data.get('User_Emp_Code', ''),
            User_Name=request.data.get('User_Name', ''),
            User_Password=request.data.get('User_Password', ''),
            User_Email=request.data.get('User_Email', ''),
            User_NICNo=request.data.get('User_NICNo', ''),
            User_TelNo=request.data.get('User_TelNo', ''),
            User_CellNo=request.data.get('User_CellNo', ''),
            User_Status=True
        )

        for obj in request.data.get('tableFormIDs', []):
            formID = obj.get('FormID')
            if formID is not None:
                formDescr = FormDescription.objects.filter(FormID=formID).first()
                UserDetail = UserLogin.objects.filter(User_ID=insertedUser.User_ID).first()
                if formDescr:
                    User_Froms.objects.create(
                        COID=1,
                        UserDetail=UserDetail,
                        FormDescription=formDescr,
                        ModuleID=formDescr.ModuleID,
                        MnuID=formDescr.MnuID,
                        MnuSubID=formDescr.MnuSubID,
                        FormSeq=formDescr.FormSeq,
                        FormStatusID=obj.get('FormStatusID', ''),
                        FormStatus=obj.get('FormStatus', ''),
                        Status=True
                    )
                else:
                    print(f"FormDescription not found for FormID: {formID}")
            else:
                print("FormID missing in obj")

        return Response("User created successfully", status=status.HTTP_201_CREATED)
    except KeyError as e:
        return Response({'error': f"Missing key in request data: {e}"}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




# @api_view(['POST'])
# def add_userprivileges(request):
#     try:
#         print('add_userprivileges')
#         print('userdata: ', request.data)
#         insertedUser = UserLogin.objects.create(
#             User_Emp_Code=request.data.get('User_Emp_Code', ''),
#             User_Name=request.data.get('User_Name', ''),
#             User_Password=request.data.get('User_Password', ''),
#             User_Email=request.data.get('User_Email', ''),
#             User_NICNo=request.data.get('User_NICNo', ''),
#             User_TelNo=request.data.get('User_TelNo', ''),
#             User_CellNo=request.data.get('User_CellNo', ''),
#             User_Status=True
#         )
#         print('insertedUser: ', insertedUser)

#         for obj in request.data.get('tableFormIDs', []):
#             print('obj: ', obj)
#             print('frmdd: ', obj.get('FormID'))
#             formDescr = FormDescription.objects.filter(FormID=obj.get('FormID')).first() 
#             print('formDescr FormID: ', formDescr)
#             print('formDescr FormID: ', formDescr.FormID)
#             print('insertedUser.User_ID: ', insertedUser.User_ID)
#             print('formDescr MnuSubID: ', formDescr.MnuSubID)
#             print('formDescr MnuSubID: ', formDescr.MnuSubID)
#             print('formDescr FormSeq: ', obj.get('FormStatusID', ''))
#             print('formDescr FormSeq: ', obj.get('FormStatus', ''))
#             User_Froms.objects.create(
#                 COID=1,
#                 User_ID=insertedUser.User_ID,
#                 FormID=obj.get('FormID', 1),
#                 ModuleID=formDescr.ModuleID,
#                 MnuID=formDescr.MnuID,
#                 MnuSubID=formDescr.MnuSubID,
#                 FormSeq=formDescr.FormSeq,
#                 FormStatusID=obj.get('FormStatusID', ''),
#                 FormStatus=obj.get('FormStatus', ''),
#                 Status=True
#             )

#         return Response("User created successfully", status=status.HTTP_201_CREATED)
#     except FormDescription.DoesNotExist:
#         return Response({'error': "FormDescription with the given ID does not exist"}, status=status.HTTP_400_BAD_REQUEST)
#     except KeyError as e:
#         return Response({'error': f"Missing key in request data: {e}"}, status=status.HTTP_400_BAD_REQUEST)
#     except Exception as e:
#         return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def getall_formDescription(request):
    try:
        formdescription = FormDescription.objects.all()
        serializer = FormDescription_Serializer(formdescription, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# @api_view(['POST'])
# def add_userprivileges(request):
#     try:
#         print('add_userprivileges')
#         print('userdata: ', request.data)

#         insnertedUser = UserLogin.objects.create(User_Emp_Code=request.data['User_Emp_Code'], User_Name=request.data['User_Name'],
#                                  User_Password=request.data['User_Password'], User_Email=request.data['User_Email'],
#                                  User_NICNo=request.data['User_NICNo'], User_TelNo=request.data['User_TelNo'],
#                                  User_CellNo=request.data['Cell_No'], User_Status=True)

#         print('insnertedUser: ', insnertedUser)

#         for obj in request.data['tableFormIDs']:
#             print('obj: ', obj)
#             formDescr = FormDescription.objects.get(pk=obj['FormID'])
#             User_Froms.objects.create(UserRoleID=1, UserID=insnertedUser.User_ID, FormID=obj['FormID'], ModuleID=formDescr.ModuleID, MnuID=formDescr.MnuID, MnuSubID=formDescr.MnuSubID,
#                                       FormSeq=formDescr.FormSeq, FormStatusID=obj['FormStatusID'], FormStatus=obj['FormStatus'], Status=True)

#             # User_Froms.objects.create(1, insnertedUser.User_ID, FormID=obj['FormID'], ModuleID=formDescr.ModuleID, MnuID=formDescr.MnuID, MnuSubID=formDescr.MnuSubID,
#             #                           FormSeq=formDescr.FormSeq, FormStatusID=obj['FormStatusID'], FormStatus=obj['FormStatus'], Status=True)

#         return Response("User privileges added successfully", status=status.HTTP_201_CREATED)
#     except Exception as e:
#         return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# @api_view(['POST'])
# def insert_userprivileges(request):
#     try:
#         print('userdata: ', request.data)
#         # serializer = HR_Department_Serializer(data=request.data)
#         if serializer.is_valid():
#             new_Department = serializer.save()
#             serialized_data = HR_Department_Serializer(new_Department).data
#             return Response(serialized_data, status=status.HTTP_201_CREATED)

#         return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

#     except Exception as e:
#         return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

