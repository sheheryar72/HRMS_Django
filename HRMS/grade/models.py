from django.db import models

class HR_Grade(models.Model):
    Grade_ID = models.AutoField(primary_key=True)
    Grade_Descr = models.CharField(max_length=100, blank=True)

    class Meta: 
        db_table = 'HR_Grade'
        managed = False  # This tells Django not to manage the table

    def __str__(self):
        return self.Grade_Descr
    

    



