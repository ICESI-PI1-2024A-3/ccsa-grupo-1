import json
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from datetime import datetime

from AcademicProgrammingApplication.models import User, Class, Subject, Teacher
from django.test import TestCase
from django.urls import reverse
from AcademicProgrammingApplication.views.edit_info_class import process_data, update_class_schedule



class EditInfoClassViewTestCase(TestCase):
    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(username='testuser', password='12345')
        # Create a teacher
        self.teacher = Teacher.objects.create(id='12345', name='Test Teacher', email='teacher@test.com',
                                              cellphone='1234567890', city='Test City', state='ACTIVO')
        # Create a subject
        self.subject = Subject.objects.create(name='Test Subject', nrc='12345', credits=3, type='CURRICULAR',
                                              start_date=datetime.now(), ending_date=datetime.now(), modality='PRESENCIAL',
                                              num_sessions=15)
        # Create a class
        self.class_instance = Class.objects.create(id='1', start_date=datetime.now(), ending_date=datetime.now(),
                                                    modality='PRESENCIAL', classroom='Aula 101', link='',
                                                    send_email=True, subject=self.subject, teacher=self.teacher)

    def test_edit_info_class_page(self):
        # Login the user
        self.client.login(username='1002959774', password='catb')
        # Get the edit-info-class page
        response = self.client.get(reverse('edit_info_class', kwargs={'class_id': self.class_instance.id}))
        # Check that the status code is 302
        self.assertEqual(response.status_code,302)

    def test_edit_info_class_post(self):
        # Login the user
        self.client.login(username='testuser', password='12345')
        # Post data to the edit-info-class page
        response = self.client.post(reverse('edit_info_class', kwargs={'class_id': self.class_instance.id}),
                                    {'action': 'save'})
        # Check that the response is a redirect
        self.assertEqual(response.status_code, 302)

    def test_process_data_function(self):
        data_json = {
            'code_materia': self.class_instance.subject.code,
            'code_clase': self.class_instance.id,
            'datetime1': self.class_instance.start_date.isoformat(),
            'datetime2': self.class_instance.ending_date.isoformat(),
            'salon': self.class_instance.classroom,
            'modality': self.class_instance.modality
        }
        processed_data = process_data(data_json)
        self.assertEqual(processed_data, [self.subject.code, str(self.class_instance.id),
                                           data_json['datetime1'], data_json['datetime2'],
                                           self.class_instance.classroom, self.class_instance.modality])

    def test_update_class_schedule_missing_data(self):
        # Definir un objeto JSON con datos faltantes para pasar a la función
        data_json = {
            'code_clase': self.class_instance.id,
            'datetime1': '2024-05-05T12:00:00'
            # Faltan 'datetime2' y 'modality'
        }
        # Verificar que la función levanta una excepción KeyError cuando faltan datos requeridos
        with self.assertRaises(KeyError):
            update_class_schedule(data_json)

    def test_edit_class_date_information(self):
        url = reverse('edit_class_date_information')
        new_start_date = timezone.now() + timezone.timedelta(days=1)
        data = {
            'code_clase': self.class_instance.id,
            'datetime1': new_start_date.isoformat(),
        }
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.class_instance.refresh_from_db()
        self.assertEqual(self.class_instance.start_date, new_start_date)

    def test_update_end_date_class(self):
        url = reverse('update_end_date_class')
        new_end_date = timezone.now() + timezone.timedelta(days=1)
        data = {
            'code_clase': self.class_instance.id,
            'datetime1': new_end_date.isoformat(),
        }
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.class_instance.refresh_from_db()
        self.assertEqual(self.class_instance.ending_date, new_end_date)