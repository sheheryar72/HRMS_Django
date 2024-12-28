from rest_framework import serializers
from .models import HR_Emp_Monthly_Sal_Mstr, HR_Emp_Monthly_Sal_Dtl

class HR_Emp_Monthly_Sal_Mstr_Serializer(serializers.ModelSerializer):
    class Meta:
        model = HR_Emp_Monthly_Sal_Mstr
        fields = '__all__'

class HR_Emp_Monthly_Sal_Dtl_Serializer(serializers.ModelSerializer):
    class Meta:
        model = HR_Emp_Monthly_Sal_Dtl
        fields = '__all__'




