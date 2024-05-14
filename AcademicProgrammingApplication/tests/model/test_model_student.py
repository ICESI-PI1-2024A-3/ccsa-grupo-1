from django.test import TestCase  # Importing necessary modules
from AcademicProgrammingApplication.models import Student  # Importing Student model


class StudentModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        """
        Creates a Student object for testing.
        """
        cls.student = Student.objects.create(
            name='Juan Pérez',
            student_id='12345',
            id_type='Cédula de ciudadanía',
            email='juan@example.com'
        )

    def test_student_creation(self):
        """
        Verifies that the Student object is created successfully.
        """
        self.assertEqual(Student.objects.count(), 1)

    def test_student_str(self):
        """
        Verifies that the __str__ method of Student model works correctly.
        """
        self.assertEqual(str(self.student), 'Juan Pérez')

    def test_student_name(self):
        """
        Verifies that the name attribute of Student model is correct.
        """
        self.assertEqual(self.student.name, 'Juan Pérez')

    def test_student_student_id(self):
        """
        Verifies that the student_id attribute of Student model is correct.
        """
        self.assertEqual(self.student.student_id, '12345')

    def test_student_id_type(self):
        """
        Verifies that the id_type attribute of Student model is correct.
        """
        self.assertEqual(self.student.id_type, 'Cédula de ciudadanía')

    def test_student_email(self):
        """
        Verifies that the email attribute of Student model is correct.
        """
        self.assertEqual(self.student.email, 'juan@example.com')
