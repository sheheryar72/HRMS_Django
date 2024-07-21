from django.db import models


class HR_Region(models.Model):
    REG_ID = models.AutoField(primary_key=True)
    REG_Descr = models.CharField(max_length=100)

    class Meta:
        db_table = 'HR_Region'
        managed = True
    
    def __str__(self):
        return self.REG_Descr

class HR_City(models.Model):
    CT_ID = models.AutoField(primary_key=True)
    CT_Descr = models.CharField(max_length=100, blank=True)
    REG_ID = models.ForeignKey(HR_Region, to_field='REG_ID', db_column='REG_ID', blank=True, null=True, on_delete=models.SET_NULL) 

    class Meta:
        db_table = 'HR_CITY'
        managed = False  # This tells Django not to manage the table

    def __str__(self):
        return self.CT_Descr





