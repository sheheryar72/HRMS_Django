from rest_framework import serializers
from .models import HR_Leaves
from payroll_period.serialiers import HR_FinYearMstrSerializer
from employee.serializers import HR_Employees_Serializer

class HR_Leaves_Serializer(serializers.ModelSerializer):
    # FYID = HR_FinYearMstrSerializer()
    # Emp_ID = HR_Employees_Serializer()
    # Emp_ID = serializers.SerializerMethodField()

    # def get_Employee(self, obj):
    #     employee_serializer = HR_Employees_Serializer(obj.Emp_ID, fields=['Emp_ID', 'Emp_Name', 'HR_Emp_ID'])
    #     return employee_serializer.data
    
    class Meta:
        model = HR_Leaves
        fields = '__all__'
        # depth = 1



