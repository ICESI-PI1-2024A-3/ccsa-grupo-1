import json  # Importing JSON module
from django.test import TestCase  # Importing necessary modules
from django.urls import reverse  # Importing reverse function to generate URLs
from django.utils import timezone  # Importing timezone module
from datetime import datetime  # Importing datetime module
from AcademicProgrammingApplication.models import User, Class, Subject, Teacher  # Importing relevant models
from AcademicProgrammingApplication.views.edit_info_class import process_data, \
    update_class_schedule  # Importing specific functions from views


class EditInfoClassViewTestCase(TestCase):
    def setUp(self):
        """
        Setting up initial conditions for the tests.
        """
        # Create a user
        self.user = User.objects.create_user(username='testuser', password='12345')
        # Create a teacher
        self.teacher = Teacher.objects.create(id='12345', name='Test Teacher', email='teacher@test.com',
                                              cellphone='1234567890', city='Test City', state='ACTIVO')
        # Create a subject
        self.subject = Subject.objects.create(name='Test Subject', nrc='12345', credits=3, type='CURRICULAR',
                                              start_date=datetime.now(), ending_date=datetime.now(),
                                              modality='PRESENCIAL',
                                              num_sessions=15)
        # Create a class
        self.class_instance = Class.objects.create(id='1', start_date=datetime.now(), ending_date=datetime.now(),
                                                   modality='PRESENCIAL', classroom='Aula 101', link='',
                                                   send_email=True, subject=self.subject, teacher=self.teacher)

    def test_edit_info_class_page(self):
        """
        Tests the GET request to the edit_info_class view.
        """
        # Login the user
        self.client.login(username='1002959774', password='catb')
        # Get the edit_info_class page
        response = self.client.get(reverse('edit_info_class', kwargs={'class_id': self.class_instance.id}))
        # Check that the status code is 302
        self.assertEqual(response.status_code, 302)

    def test_edit_info_class_post(self):
        """
        Tests the POST request to the edit_info_class view.
        """
        # Login the user
        self.client.login(username='testuser', password='12345')
        # Post data to the edit_info_class view
        response = self.client.post(reverse('edit_info_class', kwargs={'class_id': self.class_instance.id}),
                                    {'action': 'save'})
        # Check that the response is a redirect
        self.assertEqual(response.status_code, 302)

    def test_process_data_function(self):
        """
        Tests the process_data function.
        """
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
        """
        Tests the update_class_schedule function with missing data.
        """
        # Define a JSON object with missing data to pass to the function
        data_json = {
            'code_clase': self.class_instance.id,
            'datetime1': '2024-05-05T12:00:00'
            # 'datetime2' and 'modality' are missing
        }
        # Verify that the function raises a KeyError exception when required data is missing
        with self.assertRaises(KeyError):
            update_class_schedule(data_json)

    def test_edit_class_date_information(self):
        """
        Tests the edit_class_date_information view.
        """
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
        """
        Tests the update_end_date_class view.
        """
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
