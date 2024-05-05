import json
from django.test import TestCase, Client
from AcademicProgrammingApplication.models import User, Teacher, Viatic

class SaveViaticTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')
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
        data = {
            'id_teacher': self.teacher.id,
            'tiquetes': 'Si',
            'hotel': 'Si',
            'viatico': 'Si'
        }
        response = self.client.post('/save_viatic/', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {'message': 'Viatico creado exitosamente'})

    def test_invalid_method(self):
        response = self.client.get('/save_viatic/')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'error': 'Invalid method'})