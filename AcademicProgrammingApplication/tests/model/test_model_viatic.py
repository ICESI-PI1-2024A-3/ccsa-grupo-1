from django.test import TestCase  # Importing necessary modules
from django.core.files.uploadedfile import SimpleUploadedFile  # Importing SimpleUploadedFile
from AcademicProgrammingApplication.models import Viatic, Teacher  # Importing relevant models

class ViaticModelTest(TestCase):  # Defining a test case class for Viatic model
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

    def test_viatic_creation(self):  # Test for Viatic object creation
        # Creating a Viatic object for testing
        viatic_obj = Viatic.objects.create(
            transport=True,
            accommodation=False,
            viatic=True,
            viatic_status='NO_ENVIADA',
            id_teacher=self.teacher,
        )
        # Verifying that the Viatic object is created successfully
        self.assertEqual(Viatic.objects.count(), 1)

    def test_viatic_str(self):  # Test for __str__ method of Viatic model
        # Creating a Viatic object for testing
        viatic_obj = Viatic.objects.create(
            transport=True,
            accommodation=False,
            viatic=True,
            viatic_status='NO_ENVIADA',
            id_teacher=self.teacher,
        )
        # Verifying that the __str__ method of Viatic model works correctly
        self.assertEqual(str(viatic_obj), 'Transporte: Sí, Alojamiento: No, Viático: Sí, Estado del viático: No Enviada')

    def test_viatic_attributes(self):  # Test for attributes of Viatic model
        # Creating a Viatic object for testing
        viatic_obj = Viatic.objects.create(
            transport=True,
            accommodation=False,
            viatic=True,
            viatic_status='NO_ENVIADA',
            id_teacher=self.teacher,
        )
        # Verifying that the attributes of Viatic model are correct
        self.assertEqual(viatic_obj.transport, True)
        self.assertEqual(viatic_obj.accommodation, False)
        self.assertEqual(viatic_obj.viatic, True)
        self.assertEqual(viatic_obj.viatic_status, 'NO_ENVIADA')
        self.assertEqual(viatic_obj.id_teacher, self.teacher)