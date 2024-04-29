from django.test import TestCase, Client
from django.contrib.auth.models import User
from AcademicProgrammingApplication.models import Teacher, Contract

class TeacherManagementTest(TestCase):
    def setUp(self):
        
        self.user = User.objects.create_user(username='testuser', password='12345')
        
        self.teacher = Teacher.objects.create(id='1', name='Test Teacher', email='test@example.com', cellphone='1234567890', city='Test City', state='ACTIVO', picture='pictures/test.jpg')
        self.contract = Contract.objects.create(contract_status='ACTIVO', contact_preparation_date='2024-01-01', id_teacher=self.teacher)

    def test_teacher_management(self):
        self.client.login(username='testuser', password='12345')

        response = self.client.get('/teacher_management/', {'teacher_search': 'Test Teacher'})

        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.context['title'], 'Gestión de Profesores')
        self.assertEqual(response.context['user_name'], 'testuser')
        self.assertEqual(response.context['teachers'][0], self.teacher)
