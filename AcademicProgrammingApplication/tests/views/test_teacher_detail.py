# Importing necessary modules
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from AcademicProgrammingApplication.models import User, Teacher, Contract, Class, Subject


class TeacherDetailViewTestCase(TestCase):
    def setUp(self):
        # Creating a test user and logging in
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_login(self.user)

        # Creating a test teacher and associated contract
        self.teacher = Teacher.objects.create(id='123', name='Test Teacher', email='test@example.com',
                                              cellphone='123456789', city='Test City', state='ACTIVO')
        self.contract = Contract.objects.create(contract_status='ACTIVO', contact_preparation_date='2024-04-29',
                                                id_teacher=self.teacher)

        # Creating a test subject
        self.subject = Subject.objects.create(name='Test Subject', nrc='12345', credits=3, type='CURRICULAR',
                                              start_date=timezone.now(), ending_date=timezone.now(),
                                              modality='PRESENCIAL', num_sessions=15)

        # Creating a test class session associated with the teacher and subject
        self.class_session = Class.objects.create(id='1', start_date=timezone.now(),
                                                  ending_date=timezone.now(), modality='PRESENCIAL',
                                                  classroom='Test Classroom', subject=self.subject,
                                                  teacher=self.teacher)

    def test_teacher_detail_view(self):
        # Getting the URL for the teacher detail view
        url = reverse('teacher_detail', args=[self.teacher.id])
        # Sending a GET request to the teacher detail view
        response = self.client.get(url)

        # Verifying that the response is successful
        self.assertEqual(response.status_code, 200)

        # Verifying that the logged-in user's username is in the context
        self.assertEqual(response.context['user_name'], self.user.username)

        # Verifying that the teacher information is displayed correctly in the response
        self.assertContains(response, self.teacher.name)
        self.assertContains(response, self.teacher.email)
        self.assertContains(response, self.teacher.cellphone)
        self.assertContains(response, self.teacher.city)

        # Verifying that the contract information is displayed correctly in the response
        self.assertContains(response, self.contract.contract_status)

        # Verifying that the subject and class session information is displayed correctly in the response
        self.assertContains(response, self.subject.name)
        self.assertContains(response, self.class_session.start_date.strftime('%Y-%m-%dT%H:%M:%S'))
        self.assertContains(response, self.class_session.ending_date.strftime('%Y-%m-%dT%H:%M:%S'))
