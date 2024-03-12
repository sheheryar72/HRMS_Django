from rest_framework import serializers
from .models import HR_FinYearMstr, HR_PAYROLL_MONTH, HR_PAYROLL_PERIOD

class HR_FinYearMstrSerializer(serializers.ModelSerializer): 
    class Meta:
        model = HR_FinYearMstr
        fields = "__all__"

class HR_PAYROLL_MONTH_Serializer(serializers.ModelSerializer): 
    class Meta:
        model = HR_PAYROLL_MONTH
        fields = "__all__"

class HR_PAYROLL_PERIOD_Serializer(serializers.ModelSerializer): 
    # FinYear = HR_FinYearMstrSerializer()
    # payrollmonth = HR_PAYROLL_MONTH_Serializer()
    class Meta:
        model = HR_PAYROLL_PERIOD
        fields = "__all__"
        depth = 1



