from rest_framework import serializers
from .models import UserLogin

class User_Login_Serializer(serializers.ModelSerializer):
    class Meta:
        model = UserLogin
        fields = '__all__'

