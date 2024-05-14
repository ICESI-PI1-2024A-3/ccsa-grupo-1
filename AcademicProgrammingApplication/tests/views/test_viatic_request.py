import json
from django.test import TestCase, Client
from AcademicProgrammingApplication.models import User, Teacher, Viatic


class SaveViaticTest(TestCase):
    def setUp(self):
        # Creating a test client and a test user
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        # Logging in as the test user
        self.client.login(username='testuser', password='12345')
        # Creating a test teacher
        self.teacher = Teacher.objects.create(
            id='123',
            name='Profesor Prueba',
            email='profesor@prueba.com',
            cellphone='1234567890',
            city='Cali',
            state='ACTIVO',
            picture='pictures/profesor.jpg'
        )

    def test_save_viatic(self):
        # Creating test data for viatic creation
        data = {
            'id_teacher': self.teacher.id,
            'tiquetes': 'Si',
            'hotel': 'Si',
            'viatico': 'Si'
        }
        # Sending a POST request to save_viatic view with JSON data
        response = self.client.post('/save_viatic/', data=json.dumps(data), content_type='application/json')
        # Verifying that the response is successful and contains the expected message
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {'message': 'Viatico creado exitosamente'})

    def test_invalid_method(self):
        # Sending a GET request to save_viatic view, which is invalid
        response = self.client.get('/save_viatic/')
        # Verifying that the response status code is 400 (Bad Request) and contains the expected error message
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'error': 'Invalid method'})
