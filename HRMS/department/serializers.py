from rest_framework import serializers
from .models import HR_Department

class HR_Department_Serializer(serializers.ModelSerializer): 
    class Meta:
        model = HR_Department
        fields = "__all__"


