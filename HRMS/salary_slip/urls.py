from django.urls import path
from .views import get_salary_slip_by_id, generate_pdf

urlpatterns = [
    path('<int:emp_id>', get_salary_slip_by_id, name='get_salary_slip_by_id'),
    path('pdf', generate_pdf, name='generate_pdf'),
]