from django.test import TestCase, RequestFactory  # Importing necessary modules
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from django.http import JsonResponse
from AcademicProgrammingApplication.models import Teacher, Class, Subject  # Importing relevant models
from AcademicProgrammingApplication.views import assign_teacher, get_classes  # Importing relevant views
import json

class AssignTeacherTestCase(TestCase):  # Defining a test case class for the 'assign_teacher' view
    def setUp(self):  # Setting up initial conditions for each test
        self.factory = RequestFactory()  # Creating a request factory
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='password')  # Creating a user
        self.teacher = Teacher.objects.create(id='1', name='Test Teacher', email='teacher@example.com', cellphone='123456789', city='Test City', state='Activo', picture='test.jpg')  # Creating a teacher

    def test_assign_teacher_view(self):  # Test case for the 'assign_teacher' view
        url = reverse('assign_teacher')  # Getting the URL for the view
        request = self.factory.get(url)  # Creating a GET request
        request.user = self.user  # Setting the user for the request
        response = assign_teacher(request)  # Sending the request to the view function
        self.assertEqual(response.status_code, 200)  # Checking if response status code is 200
        self.assertContains(response, 'Asignar Profesor a Clase')  # Checking if 'Asignar Profesor a Clase' is present in the response

    def test_assign_teacher_with_query(self):  # Test case for the 'assign_teacher' view with query
        url = reverse('assign_teacher')  # Getting the URL for the view
        request = self.factory.get(url, {'search': 'Test'})  # Creating a GET request with query parameter
        request.user = self.user  # Setting the user for the request
        response = assign_teacher(request)  # Sending the request to the view function
        self.assertEqual(response.status_code, 200)  # Checking if response status code is 200
        self.assertContains(response, 'Asignar Profesor a Clase')  # Checking if 'Asignar Profesor a Clase' is present in the response
        self.assertIn(b'Test Teacher', response.content)  # Checking if 'Test Teacher' is present in the response content

class GetClassesTestCase(TestCase):  # Defining a test case class for the 'get_classes' view
    def setUp(self):  # Setting up initial conditions for each test
        self.factory = RequestFactory()  # Creating a request factory
        self.teacher = Teacher.objects.create(id='1', name='Test Teacher', email='teacher@example.com', cellphone='123456789', city='Test City', state='Activo', picture='test.jpg')  # Creating a teacher
        self.subject = Subject.objects.create(  # Creating a subject with required fields
            name='Test Subject',
            nrc='12345',  
            credits=3,
            type='CURRICULAR',
            syllabus='syllabus.pdf',
            start_date=timezone.now(),
            ending_date=timezone.now(),
            modality='VIRTUAL',
            num_sessions=20,
        )
        self.class_obj = Class.objects.create(  # Creating a class associated with the teacher and subject
            id='1',
            start_date='2024-01-01',
            ending_date='2024-01-05',
            modality='VIRTUAL',
            classroom='Test Classroom',
            link='https://example.com',
            subject=self.subject,
            teacher=self.teacher
        )

    def test_get_classes_view(self):  # Test case for the 'get_classes' view
        url = reverse('get_classes', kwargs={'teacher_id': self.teacher.id})  # Getting the URL for the view with teacher id as parameter
        request = self.factory.get(url)  # Creating a GET request
        response = get_classes(request, teacher_id=self.teacher.id)  # Sending the request to the view function
        self.assertEqual(response.status_code, 200)  # Checking if response status code is 200
        result = json.loads(response.content)  # Parsing JSON response
        self.assertEqual(result['messages'], 'Success')  # Checking if 'messages' key in the response is 'Success'
        self.assertEqual(result['clases'][0]['id'], '1')  # Checking if the id of the first class in the response matches expected value