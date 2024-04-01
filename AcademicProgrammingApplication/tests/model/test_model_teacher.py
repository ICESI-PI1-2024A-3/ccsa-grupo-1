from django.test import TestCase  # Importing necessary modules
from django.core.files.uploadedfile import SimpleUploadedFile  # Importing SimpleUploadedFile
from AcademicProgrammingApplication.models import Teacher  # Importing Teacher model

class TeacherModelTest(TestCase):  # Defining a test case class for Teacher model
    def setUp(self):  # Setting up initial conditions for each test
        # Creating a Teacher object for testing
        self.teacher = Teacher.objects.create(
            id='123456',
            name='Profesor de prueba',
            email='profesor@prueba.com',
            cellphone='1234567890',
            city='Ciudad de prueba',
            state='ACTIVO',
            picture=SimpleUploadedFile("file.jpg", b"file_content", content_type="image/jpeg"),  # Creating a SimpleUploadedFile object for picture
        )

    def test_teacher_creation(self):  # Test for Teacher object creation
        # Verifying that the Teacher object is created successfully
        self.assertEqual(Teacher.objects.count(), 1)

    def test_teacher_str(self):  # Test for __str__ method of Teacher model
        # Verifying that the __str__ method of Teacher model works correctly
        self.assertEqual(str(self.teacher), 'Profesor de prueba')

    def test_teacher_attributes(self):  # Test for attributes of Teacher model
        # Verifying that the attributes of Teacher model are correct
        self.assertEqual(self.teacher.id, '123456')
        self.assertEqual(self.teacher.name, 'Profesor de prueba')
        self.assertEqual(self.teacher.email, 'profesor@prueba.com')
        self.assertEqual(self.teacher.cellphone, '1234567890')
        self.assertEqual(self.teacher.city, 'Ciudad de prueba')
        self.assertEqual(self.teacher.state, 'ACTIVO')