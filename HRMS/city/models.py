from django.db import models

class HR_City(models.Model):
    CT_ID = models.AutoField(primary_key=True)
    CT_Descr = models.CharField(max_length=100, blank=True)

    class Meta:
        db_table = 'HR_CITY'
        managed = False  # This tells Django not to manage the table

    def __str__(self):
        return self.CT_Descr
    

    



