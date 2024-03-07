from rest_framework import serializers
from .models import HR_Grade

class HR_Grade_Serializer(serializers.ModelSerializer): 
    class Meta:
        model = HR_Grade
        fields = "__all__"


