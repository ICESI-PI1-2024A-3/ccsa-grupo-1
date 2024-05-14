from django.test import TestCase  # Importing necessary modules
from django.core.files.uploadedfile import SimpleUploadedFile  # Importing SimpleUploadedFile
from django.core.exceptions import ValidationError  # Importing ValidationError
from AcademicProgrammingApplication.models import Class, Subject, Teacher  # Importing relevant models


class ClassModelTest(TestCase):  # Defining a test case class for Class model
    def setUp(self):
        """
            Setting up initial conditions for each test.
            Creates Subject and Teacher objects for testing.
        """
        self.subject = Subject.objects.create(
            name='Matemáticas',
            nrc='12345',
            credits=3,
            type='CURRICULAR',
            syllabus=SimpleUploadedFile("file.pdf", b"file_content", content_type="application/pdf"),
            # Creating a SimpleUploadedFile object for syllabus
            start_date='2022-01-01',
            ending_date='2022-06-01',
            modality='PRESENCIAL',
            num_sessions=48,
        )
        self.teacher = Teacher.objects.create(
            id='123456',
            name='Profesor de prueba',
            email='profesor@prueba.com',
            cellphone='1234567890',
            city='Ciudad de prueba',
            state='ACTIVO',
            picture=SimpleUploadedFile("file.jpg", b"file_content", content_type="image/jpeg"),
            # Creating a SimpleUploadedFile object for picture
        )

    def test_class_creation(self):
        """
        Test for creating a Class object.
        Verifies that the Class object is created successfully.
        """
        class_obj = Class.objects.create(
            id='123',
            start_date='2022-01-01T00:00:00Z',
            ending_date='2022-06-01T00:00:00Z',
            modality='PRESENCIAL',
            classroom='Aula 101',
            subject=self.subject,
            teacher=self.teacher,
        )
        # Verifying that the Class object is created successfully
        self.assertEqual(Class.objects.count(), 1)

    def test_class_str(self):
        """
        Test for __str__ method of Class model.
        Verifies that the __str__ method of Class model works correctly.
        """
        # Creating a Class object for testing
        class_obj = Class.objects.create(
            id='123',
            start_date='2022-01-01T00:00:00Z',
            ending_date='2022-06-01T00:00:00Z',
            modality='PRESENCIAL',
            classroom='Aula 101',
            subject=self.subject,
            teacher=self.teacher,
        )
        # Verifying that the __str__ method of Class model works correctly
        self.assertEqual(str(class_obj), '123')

    def test_class_save_validation_error(self):
        """
        Test for validation error on saving Class object. Verifies that a validation error is raised when trying to
        save a Class object with 'PRESENCIAL' modality but without classroom.
        """
        # Trying to create a Class object with 'PRESENCIAL' modality but without classroom
        with self.assertRaises(ValidationError):
            class_obj = Class.objects.create(
                id='123',
                start_date='2022-01-01T00:00:00Z',
                ending_date='2022-06-01T00:00:00Z',
                modality='PRESENCIAL',
                classroom=None,
                subject=self.subject,
                teacher=self.teacher,
            )
