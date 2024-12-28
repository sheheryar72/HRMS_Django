from rest_framework import serializers
from .models import HR_Designation

class HR_Designation_Serializer(serializers.ModelSerializer): 
    class Meta:
        model = HR_Designation
        fields = "__all__"


