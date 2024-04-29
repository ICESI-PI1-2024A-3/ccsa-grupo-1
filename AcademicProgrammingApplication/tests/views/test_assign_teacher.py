# Import necessary modules and functions
from django.test import TestCase, RequestFactory
from django.urls import reverse
from datetime import datetime, timedelta
from AcademicProgrammingApplication.models import User, Teacher, Class, Subject
from AcademicProgrammingApplication.views import assign_teacher


# Define a test class inheriting from Django's TestCase class
class AssignTeacherViewTest(TestCase):
    # Set up initial data for the tests
    def setUp(self):
        # Create a test user
        self.user = User.objects.create(username='testuser')
        # Create a test teacher
        self.teacher = Teacher.objects.create(
            id='1',
            name='Test Teacher',
            email='test@example.com',
            cellphone='123456789',
            city='Test City',
            state='ACTIVO'
        )
        # Create a test subject
        self.subject = Subject.objects.create(
            name='Test Subject',
            nrc='123456',
            credits=3,
            type='CURRICULAR',
            start_date=datetime.now().date(),
            ending_date=(datetime.now() + timedelta(days=90)).date(),
            modality='PRESENCIAL',
            num_sessions=10
        )
        # Create a test class
        self.new_class = Class.objects.create(
            id='1',
            start_date=datetime.now(),
            ending_date=datetime.now() + timedelta(hours=2),
            modality='PRESENCIAL',
            subject=self.subject,
            teacher=self.teacher,
            classroom='Test Classroom'
        )
        # Create a RequestFactory object for generating fake HTTP requests
        self.factory = RequestFactory()

    # Define a test method for GET requests to the assign_teacher view
    def test_assign_teacher_get(self):
        # Create a fake GET request
        request = self.factory.get('/assign/1/')
        request.user = self.user
        # Call the view with the created request
        response = assign_teacher(request, class_id='1')
        # Verify that the response is successful (status code 200)
        self.assertEqual(response.status_code, 200)

    # Define a test method for POST requests to the assign_teacher view
    def test_assign_teacher_post(self):
        # Create a fake POST request
        request = self.factory.post('/assign/1/', {'teacher_id': '1'})
        request.user = self.user
        # Call the view with the created request
        response = assign_teacher(request, class_id='1')
        # Verify that the response redirects correctly
        self.assertEqual(response.status_code, 302)
        # Verify that the redirection is to the class edit page
        self.assertEqual(response.url, reverse('edit_info_class', kwargs={'class_id': '1'}))
