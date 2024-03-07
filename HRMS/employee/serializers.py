from rest_framework import serializers
from .models import HR_Employees

class HR_Employees_Serializer(serializers.ModelSerializer): 
    class Meta:
        model = HR_Employees
        fields = "__all__"



