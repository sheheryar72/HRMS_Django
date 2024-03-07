from django.test import TestCase
from django.db import connection
from .models import *

class CityTestCases(TestCase):
    
    def setup(self):
        pass

    # def test_city_creating(self):
    #     City = HR_City.objects.create('Turkey')
    #     self.assertEqual(HR_City.objects.count(), 1)

    def test_first_case(self):
        self.assertEqual(1,1)

    def test_city_count(self):
        obj = HR_City.objects.all()
        self.assertEqual(obj.count(), 37)

