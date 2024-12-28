from django.shortcuts import render
from django.db import connection
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import HR_Grade
from .serializers import HR_Grade_Serializer
from rest_framework.generics import ListCreateAPIView

def Grade_view(request):
    print('Grade called')
    return render(request, 'grade.html')

class GradeListCreateAPIView(ListCreateAPIView):
    queryset = HR_Grade.objects.all()
    serializer_class = HR_Grade_Serializer

# @api_view(['GET'])
# def get_all_grade(request):
#     try:
#         with connection.cursor() as cursor:
#             cursor.execute("SELECT * FROM HR_Grade")
#             grades = cursor.fetchall()
#             print('grades: ', grades)
#         if not grades:
#             return Response(status=status.HTTP_204_NO_CONTENT)

#         grades = [HR_Grade(Grade_ID = grade[0], Grade_Descr = grade[1]) for grade in grades]

#         serializer = HR_Grade_Serializer(grades, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     except Exception as e:
#         return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# # @api_view(['GET'])
# # def get_all_grade(request):
#     try:
#         grades = HR_Grade.objects.all()

#         if not grades:
#             return Response(status=status.HTTP_204_NO_CONTENT)

        
#         #grade_objects = [HR_Grade(Grade_ID=grade.Grade_ID, Grade_Descr=grade.Grade_Descr) for grade in grades]
#         #serializer = HR_Grade_Serializer(grade_objects, many=True)
        
#         serializer = HR_Grade_Serializer(grades, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     except Exception as e:
#         return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def get_grade_by_id(request, grade_id):
    try:
        try:
            grade = HR_Grade.objects.get(pk=grade_id)
        except HR_Grade.DoesNotExist:
            return Response({'error': 'Grade not found'}, status=status.HTTP_404_NOT_FOUND)

        grade_object = HR_Grade(Grade_ID=grade.Grade_ID, Grade_Descr=grade.Grade_Descr)
        serializer = HR_Grade_Serializer(grade_object)
        return Response(serializer.data, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def insert_grade(request):
    try:
        serializer = HR_Grade_Serializer(data=request.data)
        if serializer.is_valid():
            new_Grade = serializer.save()
            serialized_data = HR_Grade_Serializer(new_Grade).data
            return Response(serialized_data, status=status.HTTP_201_CREATED)

        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['PUT'])
def update_grade(request, grade_id):
    try:
        grade = HR_Grade.objects.get(pk=grade_id)
    except HR_Grade.DoesNotExist:
        return Response({'error': 'Grade not found'}, status=status.HTTP_404_NOT_FOUND)
    
    try:
        serializer = HR_Grade_Serializer(grade, data=request.data, partial=True)
        if serializer.is_valid():
            updated_Grade = serializer.save()
            serialized_data = HR_Grade_Serializer(updated_Grade).data
            return Response(serialized_data, status=status.HTTP_200_OK)

        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['DELETE'])
def delete_grade(request, grade_id):
    try:
        Grade = HR_Grade.objects.get(pk=grade_id)
    except HR_Grade.DoesNotExist:
        return Response({'error': 'Grade not found'}, status=status.HTTP_404_NOT_FOUND)

    try:
        Grade.delete()
        return Response({'message': 'Grade deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    