from rest_framework import serializers
from .models import HR_Monthly_All_Ded

class HR_Monthly_All_Ded_Serializer(serializers.ModelSerializer):
    class Meta:
        model = HR_Monthly_All_Ded
        fields = '__all__'




