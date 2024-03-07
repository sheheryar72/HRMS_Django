from django.db import models

class HR_Department(models.Model):
    Dept_ID = models.AutoField(primary_key=True)
    Dept_Descr = models.CharField(max_length=100, blank=True)

    class Meta:
        managed = False  # This tells Django not to manage the table
        db_table = 'HR_Department'

    def __str__(self):
        return self.Dept_Descr



class MyClass:

    def __init__(self, param1, param2):
        # Initialize attributes with values passed as parameters
        self.attribute1 = param1
        self.attribute2 = param2

    def display_attributes(self):
        print(f"Attribute 1: {self.attribute1}")
        print(f"Attribute 2: {self.attribute2}")

# Creating an instance of MyClass and passing values to the constructor
my_instance = MyClass("Value1", "Value2")

# Accessing attributes and calling a method
my_instance.display_attributes()



