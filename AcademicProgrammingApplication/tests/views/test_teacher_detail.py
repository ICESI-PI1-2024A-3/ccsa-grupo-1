from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from AcademicProgrammingApplication.models import Teacher, Contract, Class, Subject

class TeacherDetailViewTestCase(TestCase):
    def setUp(self):
        
        self.user = User.objects.create(username='testuser')
        self.client.force_login(self.user)

        self.teacher = Teacher.objects.create(id='123', name='Test Teacher', email='test@example.com',
                                              cellphone='123456789', city='Test City', state='ACTIVO')
        self.contract = Contract.objects.create(contract_status='ACTIVO', contact_preparation_date='2024-04-29',
                                                id_teacher=self.teacher)

        self.subject = Subject.objects.create(name='Test Subject', nrc='12345', credits=3, type='CURRICULAR',
                                              start_date=timezone.now(), ending_date=timezone.now(),
                                              modality='PRESENCIAL', num_sessions=15)

        self.class_session = Class.objects.create(id='1', start_date=timezone.now(),
                                                   ending_date=timezone.now(), modality='PRESENCIAL',
                                                   classroom='Test Classroom', subject=self.subject,
                                                   teacher=self.teacher)

    def test_teacher_detail_view(self):
       
        url = reverse('teacher_detail', args=[self.teacher.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.context['user_name'], self.user.username)

        self.assertContains(response, self.teacher.name)
        self.assertContains(response, self.teacher.email)
        self.assertContains(response, self.teacher.cellphone)
        self.assertContains(response, self.teacher.city)

        self.assertContains(response, self.contract.contract_status)
        self.assertContains(response, self.contract.contact_preparation_date)

        self.assertContains(response, self.subject.name)
        self.assertContains(response, self.class_session.start_date.strftime('%Y-%m-%dT%H:%M:%S'))
        self.assertContains(response, self.class_session.ending_date.strftime('%Y-%m-%dT%H:%M:%S'))