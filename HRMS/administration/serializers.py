from .models import User_Froms, GroupOfCompanies, FormDescription
from rest_framework import serializers
from hr_login.serializers import User_Login_Serializer

class GroupOfCompanies_Serializer(serializers.ModelSerializer):
    class Meta:
        model = GroupOfCompanies
        fields = ['CoID', 'CoName', 'Active']

class FormDescription_Serializer(serializers.ModelSerializer):
    class Meta:
        model = FormDescription
        fields = "__all__"

class User_Froms_Serializer(serializers.ModelSerializer):
    FormDescription = FormDescription_Serializer()
    UserDetail = User_Login_Serializer()
    class Meta:
        model = User_Froms
        fields = "__all__"

