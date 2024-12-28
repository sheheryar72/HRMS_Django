from django.db import models

class HR_Designation(models.Model):
    DSG_ID = models.AutoField(primary_key=True)
    DSG_Descr = models.CharField(max_length=100, blank=True)

    class Meta:
        db_table = 'HR_Designation'
        managed = False  # This tells Django not to manage the table

    @staticmethod
    def getall_designation():
        # return HR_Designation.objects.values('DSG_ID').all()
        return HR_Designation.objects.all()
        # return HR_Designation.objects.filter(DSG_Descr__contains='HR')
    
    def __str__(self):
        return self.DSG_Descr
    

    



