from rest_framework import serializers
from .models import HR_W_All_Ded_Department

class HR_W_All_Ded_Department_Serializer(serializers.ModelSerializer):
    class Meta:
        model = HR_W_All_Ded_Department
        fields = '__all__'

