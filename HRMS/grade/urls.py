from django.urls import path
from .views import Grade_view, get_grade_by_id, insert_grade, update_grade, delete_grade, GradeListCreateAPIView

urlpatterns = [
    path('', Grade_view),
    path('getall', GradeListCreateAPIView.as_view(), name='GradeListCreateAPIView'),
    # path('getall', get_all_grade, name='get_all_grade'),
    path('getbyid/<int:grade_id>', get_grade_by_id, name='get_grade_by_id'),
    path('add', insert_grade, name='insert_grade'),
    path('update/<int:grade_id>', update_grade, name='update_grade'),
    path('delete/<int:grade_id>', delete_grade, name='delete_grade'),
]

    