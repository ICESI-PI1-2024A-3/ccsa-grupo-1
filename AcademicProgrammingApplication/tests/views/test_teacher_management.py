# Importing necessary modules
from django.test import TestCase, Client
from AcademicProgrammingApplication.models import User, Teacher, Contract


class TeacherManagementTest(TestCase):
    def setUp(self):
        # Creating a test user
        self.user = User.objects.create_user(username='testuser', password='12345')

        # Creating a test teacher and associated contract
        self.teacher = Teacher.objects.create(id='1', name='Test Teacher', email='test@example.com',
                                              cellphone='1234567890', city='Test City', state='ACTIVO',
                                              picture='pictures/test.jpg')
        self.contract = Contract.objects.create(contract_status='ACTIVO', contact_preparation_date='2024-01-01',
                                                id_teacher=self.teacher)

    def test_teacher_management(self):
        # Logging in as the test user
        self.client.login(username='testuser', password='12345')

        # Sending a GET request to teacher_management view with a search query
        response = self.client.get('/teacher_management/', {'teacher_search': 'Test Teacher'})

        # Verifying that the response is successful
        self.assertEqual(response.status_code, 200)

        # Verifying that the context contains the expected data
        self.assertEqual(response.context['title'], 'Gestión de Profesores')
        self.assertEqual(response.context['user_name'], 'testuser')
        self.assertEqual(response.context['teachers'][0], self.teacher)
