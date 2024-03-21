"""
URL configuration for HRMS project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf.urls.static import static
from django.conf import settings


schema_view = get_schema_view(
    openapi.Info(
        title="Your API",
        default_version='v1',
        description="Your API description",
        terms_of_service="https://localhost:8000/",
        contact=openapi.Contact(email="contact@yourapp.com"),
        license=openapi.License(name="Your License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('admin/', admin.site.urls),
    path('city/', include('city.urls')),
    path('department/', include('department.urls')),
    path('designation/', include('designation.urls')),
    path('grade/', include('grade.urls')),
    path('salaryslip/', include('salary_slip.urls')),
    path('employee/', include('employee.urls')),
    path('login/', include('hr_login.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('payroll_period/', include('payroll_period.urls')),
    path('administration/', include('administration.urls')),
    path('payroll_element/', include('payroll_element.urls')),
    path('leaves/', include('leaves.urls')),
    path('loan/', include('loan.urls')),
    path('wda/', include('working_dept_assignment.urls')),
    path('salaryupdate/', include('salary_update.urls')),
    path('monthly_all_ded/', include('monthly_all_ded.urls')),
    #path('report_builder/', include('report_builder.urls')),
]
# + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
