from django.test import TestCase
from .models import *
from django.urls import reverse

class DepartmentTestCase(TestCase):
    def setUp(self):
        HR_Department.objects.create(Dept_Descr='description 1')

    def test_dept_list(self):
        response = self.client.post(reverse('get_all_dept'))
        response = self.client.get(reverse('get_all_dept'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('')
        self.assertContains(response, 'description 1')
        self.assertContains(response, 'description 2')
        dept = HR_Department.objects.first()
        dept = HR_Department.objects.last()
        depts = HR_Department.objects.all()
        self.assertEqual(dept.Dept_Descr, 'description 1')
        self.assertEqual(dept.Dept_Descr, 'description 2')
        self.assertEqual(depts.count(), 2)

    def test_create_dept(self):
        response = self.client.post(reverse('create_dept'), {'description 2'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(HR_Department.objects.count(), 2)
        self.assertContains(response, 'Description 2')








