from rest_framework import serializers
from .models import Salary_Slip

class Salary_Slip_Serializer(serializers.Serializer):
    Emp_Sl_ID = serializers.IntegerField()
    Emp_Sl_Date = serializers.DateTimeField(allow_null=True)
    Emp_ID = serializers.IntegerField(allow_null=True)
    HR_Emp_ID = serializers.IntegerField()
    Dsg_ID = serializers.IntegerField()
    DSG_Descr = serializers.CharField(max_length=100)
    Dept_ID = serializers.IntegerField()
    Dept_Descr = serializers.CharField(max_length=100)
    Grade_ID = serializers.IntegerField()
    Grade_Descr = serializers.CharField(max_length=100)
    Co_ID = serializers.IntegerField()
    Month_Days = serializers.FloatField()
    Ded_Days = serializers.FloatField()
    Working_Days = serializers.FloatField()
    Leave_Bal = serializers.FloatField()
    Element_ID = serializers.IntegerField()
    Element_Name = serializers.CharField(max_length=100)
    Amount = serializers.FloatField()
    Element_Type = serializers.CharField(max_length=100)
    Element_Category = serializers.CharField(max_length=100)

    def to_representation(self, instance):
        # Convert tuple to dictionary
        return {
            'Emp_Sl_ID': instance[0],
            'Emp_Sl_Date': instance[1],
            'Emp_ID': instance[2],
            'HR_Emp_ID': instance[3],
            'Dsg_ID': instance[4],
            'DSG_Descr': instance[5],
            'Dept_ID': instance[6],
            'Dept_Descr': instance[7],
            'Grade_ID': instance[8],
            'Grade_Descr': instance[9],
            'Co_ID': instance[10],
            'Month_Days': instance[11],
            'Ded_Days': instance[12],
            'Working_Days': instance[13],
            'Leave_Bal': instance[14],
            'Element_ID': instance[15],
            'Element_Name': instance[16],
            'Amount': instance[17],
            'Element_Type': instance[18],
            'Element_Category': instance[19],
        }
