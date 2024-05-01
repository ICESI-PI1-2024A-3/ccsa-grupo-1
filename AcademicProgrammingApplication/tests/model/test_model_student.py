from django.test import TestCase
from AcademicProgrammingApplication.models import Student

class StudentModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.student = Student.objects.create(
            name='Juan Pérez',
            student_id='12345',
            id_type='Cédula de ciudadanía',
            email='juan@example.com'
        )

    def test_student_creation(self):
        self.assertEqual(Student.objects.count(), 1)

    def test_student_str(self):
        self.assertEqual(str(self.student), 'Juan Pérez')

    def test_student_name(self):
        self.assertEqual(self.student.name, 'Juan Pérez')

    def test_student_student_id(self):
        self.assertEqual(self.student.student_id, '12345')

    def test_student_id_type(self):
        self.assertEqual(self.student.id_type, 'Cédula de ciudadanía')

    def test_student_email(self):
        self.assertEqual(self.student.email, 'juan@example.com')
