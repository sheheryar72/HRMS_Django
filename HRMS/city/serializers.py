from rest_framework import serializers
from .models import HR_City

class HR_CITY_Serializer(serializers.ModelSerializer): 
    class Meta:
        model = HR_City
        #fields = ('CT_ID', 'CT_Descr')
        fields = "__all__"


