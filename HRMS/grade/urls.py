from django.urls import path
from .views import Grade_view, get_grade_by_id, insert_grade, update_grade, delete_grade, GradeListCreateAPIView

urlpatterns = [
    path('', Grade_view),
    path('api/getall', GradeListCreateAPIView.as_view(), name='GradeListCreateAPIView'),
    # path('api/getall', get_all_grade, name='get_all_grade'),
    path('api/getbyid/<int:grade_id>', get_grade_by_id, name='get_grade_by_id'),
    path('api/add', insert_grade, name='insert_grade'),
    path('api/update/<int:grade_id>', update_grade, name='update_grade'),
    path('api/delete/<int:grade_id>', delete_grade, name='delete_grade'),
]

    