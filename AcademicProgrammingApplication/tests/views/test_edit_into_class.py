from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from datetime import datetime, timedelta
from AcademicProgrammingApplication.models import User, Class, Student, Subject, Teacher
from django.test import TestCase
from django.urls import reverse
from AcademicProgrammingApplication.views.edit_info_class import process_data
import json
from django.core import mail  # Add this line
from AcademicProgrammingApplication.models import Class, Student
from AcademicProgrammingApplication.views.edit_info_class import update_class_schedule


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
        

    def test_send_email_on_save(self):
        # Create a class instance to test
        test_class = self.class_instance  

        # Make a POST request to save changes
        self.client.post(reverse('edit_info_class', kwargs={'class_id': test_class.id}), {'action': 'save'})

        



    def test_process_data_invalid_data(self):
        # Invalid JSON data to test
        invalid_data_json = {
            # Missing 'code_materia'
            'code_clase': '12345',
            'datetime1': '2024-05-05T12:00:00',
            'datetime2': '2024-05-05T13:00:00',
            'salon': 'Aula 101',
            'modality': 'PRESENCIAL'
        }

        # Verify that process_data handles incorrect data correctly
        with self.assertRaises(KeyError):
            process_data(invalid_data_json)

   
class UpdateClassScheduleTestCase(TestCase):
    # Test setup methods, such as setUp(), can be defined here
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


    

    def test_update_class_schedule_invalid_modality(self):
        # Create a class instance to test
        test_class = self.class_instance 

        # JSON data with invalid modality
        data_json = {
            'code_clase': test_class.id,
            'datetime1': '2024-05-05T12:00:00',
            'datetime2': '2024-05-05T13:00:00',
            'salon': 'Aula 101',
            'modality': 'INVALID',  # Provide an invalid modality
        }

#test_cancel_changes_redirect
class EditClassDateInformationTestCase(TestCase):
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

   

    def test_handle_valid_date(self):
        # Create a class instance to test
        test_class = self.class_instance  

        # JSON data with valid start date
        valid_data_json = {
            'code_clase': test_class.id,
            'datetime1': '2024-05-05T12:00:00',  # Provide a valid start date
        }

        # Verify that the function handles the valid start date properly
        response = self.client.post(reverse('edit_class_date_information'), data=json.dumps(valid_data_json), content_type='application/json')
        self.assertEqual(response.status_code, 200)  # Verify that an appropriate status code is returned
        

    def test_handle_invalid_date(self):
        # Create a class instance to test
        test_class = self.class_instance  

        # JSON data with invalid start date
        invalid_data_json = {
            'code_clase': test_class.id,
            # Missing 'datetime1'
        }

        # Verify that the function handles the invalid start date properly
        response = self.client.post(reverse('edit_class_date_information'), data=json.dumps(invalid_data_json), content_type='application/json')
        self.assertEqual(response.status_code, 500)  # Verify that an appropriate status code is returned
       

    def test_handle_invalid_class_id(self):
        # JSON data with invalid class ID
        invalid_data_json = {
            'code_clase': 'invalid_id',
            'datetime1': '2024-05-05T12:00:00',
        }

        # Verify that the function handles the invalid class ID properly
        response = self.client.post(reverse('edit_class_date_information'), data=json.dumps(invalid_data_json), content_type='application/json')
        self.assertEqual(response.status_code, 500)  # Verify that an appropriate status code is returned
       

class UpdateEndDateClassTestCase(TestCase):
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

    # Test setup methods, such as setUp(), can be defined here

    def test_update_end_date_class(self):
        # Create a class instance to test
        test_class = self.class_instance  

        # JSON data with valid end date
        valid_data_json = {
            'code_clase': test_class.id,
            'datetime1': '2024-05-05T12:00:00',  
        }

        # Verify that the function handles the valid end date properly
        response = self.client.post(reverse('update_end_date_class'), data=json.dumps(valid_data_json), content_type='application/json')
        self.assertEqual(response.status_code, 200)  # Verify that an appropriate status code is returned
        

    def test_update_end_date_class_invalid_date(self):
        # Create a class instance to test
        test_class = self.class_instance  

        # JSON data with invalid end date
        invalid_data_json = {
            'code_clase': test_class.id,
            
        }

        # Verify that the function handles the invalid end date properly
        response = self.client.post(reverse('update_end_date_class'), data=json.dumps(invalid_data_json), content_type='application/json')
        self.assertEqual(response.status_code, 500)  # Verify that an appropriate status code is returned
        

    def test_update_end_date_class_invalid_class_id(self):
        # JSON data with invalid class ID
        invalid_data_json = {
            'code_clase': 'invalid_id',
            'datetime1': '2024-05-05T12:00:00',
        }

        # Verify that the function handles the invalid class ID properly
        response = self.client.post(reverse('update_end_date_class'), data=json.dumps(invalid_data_json), content_type='application/json')
        self.assertEqual(response.status_code, 500)  # Verify that an appropriate status code is returned
        


class CancelChangesRedirectTestCase(TestCase):
    def setUp(self):
        # Create a subject without a syllabus
        self.subject = Subject.objects.create(
            name='Test Subject',
            nrc='123456',
            credits=3,
            type='CURRICULAR',
            start_date='2024-01-01',
            ending_date='2024-05-01',
            modality='PRESENCIAL',
            num_sessions=15
        )

    def test_cancel_changes_redirect(self):
        # Ensure that if syllabus is empty, the test still passes
        response = self.client.get(reverse('subject_detail', kwargs={'subject_id': self.subject.code}))
        self.assertEqual(response.status_code, 302) 

    def tearDown(self):
        self.subject.delete()