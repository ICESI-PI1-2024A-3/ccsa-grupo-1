from django.test import TestCase  # Importing necessary modules
from django.core.files.uploadedfile import SimpleUploadedFile  # Importing SimpleUploadedFile
from AcademicProgrammingApplication.models import Program, Semester, Subject  # Importing relevant models

class ProgramModelTest(TestCase):  # Defining a test case class for Program model
    def setUp(self):  # Setting up initial conditions for each test
        # Creating Semester and Subject objects for testing
        self.semester = Semester.objects.create(
            period='2022-1',
            start_date='2022-01-01',
            ending_date='2022-06-01',
        )
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

        # Creating a Program object for testing
        self.program = Program.objects.create(
            name='Programa de prueba',
            faculty='Facultad de Ciencias',
            director='Director de prueba',
            cost=1000.00,
            type='MAESTRÍA',
            modality='PRESENCIAL',
            duration='2 años',
            curriculum=SimpleUploadedFile("file.pdf", b"file_content", content_type="application/pdf"),  # Creating a SimpleUploadedFile object for curriculum
        )
        self.program.semesters.add(self.semester)  # Adding semester relation to the program
        self.program.subjects.add(self.subject)  # Adding subject relation to the program

    def test_program_creation(self):  # Test for Program object creation
        # Verifying that the Program object is created successfully
        self.assertEqual(Program.objects.count(), 1)

    def test_program_str(self):  # Test for __str__ method of Program model
        # Verifying that the __str__ method of Program model works correctly
        self.assertEqual(str(self.program), 'Programa de prueba')

    def test_program_attributes(self):  # Test for attributes of Program model
        # Verifying that the attributes of Program model are correct
        self.assertEqual(self.program.name, 'Programa de prueba')
        self.assertEqual(self.program.faculty, 'Facultad de Ciencias')
        self.assertEqual(self.program.director, 'Director de prueba')
        self.assertEqual(self.program.cost, 1000.00)
        self.assertEqual(self.program.type, 'MAESTRÍA')
        self.assertEqual(self.program.modality, 'PRESENCIAL')
        self.assertEqual(self.program.duration, '2 años')

    def test_program_relations(self):  # Test for relations of Program model
        # Verifying that the relations of Program model are correct
        self.assertEqual(self.program.semesters.count(), 1)
        self.assertEqual(self.program.subjects.count(), 1)