from django.db import models

# Create your models here.

class HR_FinYearMstr(models.Model):
    FYID = models.AutoField(primary_key=True)
    FinYear = models.CharField(max_length=20)
    FYStatus = models.BooleanField()
    
    class Meta:
        managed = False
        db_table = 'HR_FinYearMstr'

    def __str__(self):
        return str(self.FYID)

class HR_PAYROLL_MONTH(models.Model):
    MNTH_ID = models.AutoField(primary_key=True)
    MNTH_NO = models.IntegerField()
    MNTH_NAME = models.CharField(max_length=25)
    MNTH_SHORT_NAME = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'HR_PAYROLL_MONTH'

    def __str__(self):
        return self.MNTH_ID

class HR_PAYROLL_PERIOD(models.Model):
    ID = models.AutoField(primary_key=True)
    PERIOD_ID = models.IntegerField()
    # FYID = models.IntegerField()
    # MNTH_ID = models.IntegerField()
    PERIOD_STATUS = models.BooleanField()
    payrollmonth = models.ForeignKey(HR_PAYROLL_MONTH, to_field='MNTH_ID',  db_column='MNTH_ID', on_delete=models.CASCADE)
    FinYear = models.ForeignKey(HR_FinYearMstr, to_field='FYID',  db_column='FYID', on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'HR_PAYROLL_PERIOD'

    def __str__(self):
        return str(self.PERIOD_ID)
