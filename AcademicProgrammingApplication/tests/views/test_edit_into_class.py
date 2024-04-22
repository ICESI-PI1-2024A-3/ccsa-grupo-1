from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from AcademicProgrammingApplication.models import Class, Subject, Student
import json

class DataProcessorLoungeTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='user', password='pass')
        self.client.login(username='user', password='pass')
        
        # Create a test subject
        self.subject = Subject.objects.create(name='Test Subject', code='123')
        
        # Create a test class associated with the test subject
        self.edit_class = Class.objects.create(id='001', subject=self.subject)
        
        # Create a student associated with the test subject
        self.student = Student.objects.create(name='Test Student', subject=self.subject)
        
    def test_data_processor_lounge_post_success_presencial(self):
        # Simulate a successful POST request to process data for updating the class (presential modality)
        data = {
            'code_materia': '123',
            'code_clase': '001',
            'datetime1': '2024-04-25T08:00:00',
            'datetime2': '2024-04-25T10:00:00',
            'modality': 'presencial',
            'salon': '101D'
        }
        response = self.client.post(reverse('data_processor_lounge'), json.dumps(data), content_type='application/json')
        
        # Verify that the response is successful
        self.assertEqual(response.status_code, 200)
        
        # Verify that the data is processed correctly
        self.assertJSONEqual(response.content, {'mensaje': 'Datos procesados correctamente'})
        
        # Verify that the class modality is updated correctly to presential
        updated_class = Class.objects.get(id='001')
        self.assertEqual(updated_class.modality, 'PRESENCIAL')
        
        # Verify that the student receives an email if the class is presential
        self.assertTrue(self.student.receive_email)
        
    def test_data_processor_lounge_post_success_virtual(self):
        # Simulate a successful POST request to process data for updating the class (virtual modality)
        data = {
            'code_materia': '123',
            'code_clase': '001',
            'datetime1': '2024-04-25T08:00:00',
            'datetime2': '2024-04-25T10:00:00',
            'modality': 'virtual'
        }
        response = self.client.post(reverse('data_processor_lounge'), json.dumps(data), content_type='application/json')
        
        # Verify that the response is successful
        self.assertEqual(response.status_code, 200)
        
        # Verify that the data is processed correctly
        self.assertJSONEqual(response.content, {'mensaje': 'Datos procesados correctamente'})
        
        # Verify that the class modality is updated correctly to virtual
        updated_class = Class.objects.get(id='001')
        self.assertEqual(updated_class.modality, 'VIRTUAL')
        
        # Verify that the student does not receive an email if the class is virtual
        self.assertFalse(self.student.receive_email)
        
    def test_data_processor_lounge_post_invalid_modality(self):
        # Simulate a POST request with an invalid modality
        data = {
            'code_materia': '123',
            'code_clase': '001',
            'datetime1': '2024-04-25T08:00:00',
            'datetime2': '2024-04-25T10:00:00',
            'modality': 'online'
        }
        response = self.client.post(reverse('data_processor_lounge'), json.dumps(data), content_type='application/json')
        
        # Verify that the request returns an error
        self.assertEqual(response.status_code, 400)
        
        # Verify that the student does not receive an email if the modality is invalid
        self.assertFalse(self.student.receive_email)