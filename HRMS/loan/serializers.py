from .models import HR_Loans
from rest_framework import serializers

class HR_Loans_Serializer(serializers.ModelSerializer):
    class Meta:
        model = HR_Loans
        fields = '__all__'




