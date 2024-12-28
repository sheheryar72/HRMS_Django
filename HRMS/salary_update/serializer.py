from rest_framework import serializers
from .models import HR_Emp_Sal_Update_Mstr, HR_Emp_Sal_Update_Dtl

class HR_Emp_Sal_Update_Mstr_Serializer(serializers.ModelSerializer):
    class Meta:
        model = HR_Emp_Sal_Update_Mstr
        fields = '__all__'

class HR_Emp_Sal_Update_Dtl_Serializer(serializers.ModelSerializer):
    class Meta:
        model = HR_Emp_Sal_Update_Dtl
        fields = '__all__'




