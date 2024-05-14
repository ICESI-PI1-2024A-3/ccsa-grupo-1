# Importing necessary modules and models
from django.test import TestCase, Client
from django.utils import timezone
from django.urls import reverse
from AcademicProgrammingApplication.models import User, Semester, Program, Class, Teacher, Subject


class SubjectDetailTest(TestCase):  # Defining a test case class for subject detail view
    def setUp(self):  # Setting up initial conditions for each test
        self.client = Client()  # Creating a test client
        self.user = User.objects.create_user(username='user', password='pass')  # Creating a user
        self.client.login(username='user', password='pass')  # Logging in as the created user

        start_date = timezone.now()  # Getting current time
        ending_date = start_date + timezone.timedelta(days=90)  # Creating an ending date 90 days after start
        self.semester = Semester.objects.create(period='2024-1', start_date=start_date,
                                                ending_date=ending_date)  # Creating a semester

        self.program = Program.objects.create(name='Programa de prueba', cost=1000, duration=4,  # Creating a program
                                              faculty='Facultad de prueba', modality='Modalidad de prueba',
                                              type='Tipo de prueba', director='Director de prueba')

        # Creating a subject
        self.subject = Subject.objects.create(
            name='Materia de Prueba',
            nrc='12345',
            credits=3,
            type='CURRICULAR',
            syllabus='syllabus.pdf',
            start_date=timezone.now(),
            ending_date=timezone.now(),
            modality='PRESENCIAL',
            num_sessions=15,
            program=self.program
        )

        # Creating a teacher
        self.teacher = Teacher.objects.create(name='Profesor de Prueba')

        # Creating a class associated with the subject and teacher
        self.class1 = Class.objects.create(
            id='001',
            start_date=timezone.make_aware(timezone.datetime(2024, 3, 18, 8, 0, 0)),
            ending_date=timezone.make_aware(timezone.datetime(2024, 3, 18, 10, 0, 0)),
            modality='PRESENCIAL',
            classroom='101D',
            subject=self.subject,
            teacher=self.teacher
        )

    def test_subject_detail_view(self):  # Test case for subject detail view
        # Accessing the subject detail view
        response = self.client.get(reverse('subject_detail', args=[self.subject.code]))

        # Verifying that the response is successful
        self.assertEqual(response.status_code, 200)

        # Verifying that the subject and class information is displayed correctly in the response
        self.assertContains(response, 'Materia de Prueba')
        self.assertContains(response, '12345')
        self.assertContains(response, '3')
        self.assertContains(response, 'CURRICULAR')
        self.assertContains(response, 'PRESENCIAL')
        self.assertContains(response, '15')
        self.assertContains(response, '101D')
        self.assertContains(response, '18 de marzo de 2024 a las 08:00')
        self.assertContains(response, '18 de marzo de 2024 a las 10:00')
