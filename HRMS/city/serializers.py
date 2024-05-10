from rest_framework import serializers
from .models import HR_City, HR_Region

class HR_CITY_Serializer(serializers.ModelSerializer): 
    class Meta:
        model = HR_City
        #fields = ('CT_ID', 'CT_Descr')
        fields = "__all__"

class HR_Region_Serializer(serializers.ModelSerializer):
    class Meta:
        model = HR_Region
        fields = "__all__"


