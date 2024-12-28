from .models import *
from rest_framework import serializers

class HR_GetUserMenuAndFormsSerializer(serializers.ModelSerializer):
    class Meta:
        models = HR_GetUserMenuAndForms
        fields = '_all_'


