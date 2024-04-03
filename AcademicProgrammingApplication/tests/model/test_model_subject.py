from django.test import TestCase  # Importing necessary modules
from django.core.files.uploadedfile import SimpleUploadedFile  # Importing SimpleUploadedFile
from AcademicProgrammingApplication.models import Subject  # Importing Subject model

class SubjectModelTest(TestCase):  # Defining a test case class for Subject model
    def setUp(self):  # Setting up initial conditions for each test
        # Creating a Subject object for testing
        self.subject = Subject.objects.create(
            name='Matemáticas',
            nrc='12345',
            credits=3,
            type='CURRICULAR',
            syllabus=SimpleUploadedFile("file.pdf", b"file_content", content_type="application/pdf"),  # Creating a SimpleUploadedFile object for syllabus
            start_date='2022-01-01',
            ending_date='2022-06-01',
            modality='PRESENCIAL',
            num_sessions=48,
        )

    def test_subject_creation(self):  # Test for Subject object creation
        # Verifying that the Subject object is created successfully
        self.assertEqual(Subject.objects.count(), 1)

    def test_subject_str(self):  # Test for __str__ method of Subject model
        # Verifying that the __str__ method of Subject model works correctly
        self.assertEqual(str(self.subject), 'Matemáticas')

    def test_subject_attributes(self):  # Test for attributes of Subject model
        # Verifying that the attributes of Subject model are correct
        self.assertEqual(self.subject.name, 'Matemáticas')
        self.assertEqual(self.subject.nrc, '12345')
        self.assertEqual(self.subject.credits, 3)
        self.assertEqual(self.subject.type, 'CURRICULAR')
        self.assertEqual(self.subject.start_date, '2022-01-01')
        self.assertEqual(self.subject.ending_date, '2022-06-01')
        self.assertEqual(self.subject.modality, 'PRESENCIAL')
        self.assertEqual(self.subject.num_sessions, 48)