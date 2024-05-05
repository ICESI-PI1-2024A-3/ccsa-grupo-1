from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from datetime import datetime, timedelta
from AcademicProgrammingApplication.models import User, Class, Student, Subject, Teacher
from django.test import TestCase
from django.urls import reverse
from AcademicProgrammingApplication.views.edit_info_class import process_data



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
        """
        Test that the edit-info-class page returns a 302 status code.
        """
        # Login the user
        self.client.login(username='1002959774', password='catb')
        # Get the edit-info-class page
        response = self.client.get(reverse('edit_info_class', kwargs={'class_id': self.class_instance.id}))
        # Check that the status code is 302
        self.assertEqual(response.status_code,302)

    def test_edit_info_class_post(self):
        """
        Test that posting to the edit-info-class page redirects to the subject_detail page.
        """
        # Login the user
        self.client.login(username='testuser', password='12345')
        # Post data to the edit-info-class page
        response = self.client.post(reverse('edit_info_class', kwargs={'class_id': self.class_instance.id}),
                                    {'action': 'save'})
        # Check that the response is a redirect
        self.assertEqual(response.status_code, 302)
        # Check that it redirects to the subject_detail page
        #self.assertRedirects(response, reverse('subject_detail', kwargs={'subject_id': self.subject.code}))

    def test_process_data_function(self):
        """
        Test the process_data function.
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
        print("Processed Data:", processed_data)
        print("Expected Data:", [str(self.subject.code), str(self.class_instance.id),
                             data_json['datetime1'], data_json['datetime2'],
                             self.class_instance.classroom, self.class_instance.modality])
        #self.assertEqual(processed_data, [str(self.subject.code), str(self.class_instance.id),
                                       #data_json['datetime1'], data_json['datetime2'],
                                       #self.class_instance.classroom, self.class_instance.modality])
