from django.db import models
from rest_framework import serializers

class HR_Payroll_Elements(models.Model):
    Element_ID = models.AutoField(primary_key=True)
    Element_Name = models.CharField(max_length=50)
    Element_Type = models.CharField(max_length=50)
    Element_Category = models.CharField(max_length=50)
    Cal_Type = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'HR_Payroll_Elements'
        # app_label = 'HR_Payroll_Elements'  


class HR_Payroll_Elements_Serializer(serializers.ModelSerializer):
    class Meta:
        model = HR_Payroll_Elements
        fields = '__all__'

