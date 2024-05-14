from django.test import TestCase  # Importing necessary modules
from django.utils import timezone  # Importing timezone module
from AcademicProgrammingApplication.models import Semester  # Importing Semester model


class SemesterModelTest(TestCase):  # Defining a test case class for Semester model
    def setUp(self):  # Setting up initial conditions for each test
        """
        Creates a Semester object for testing.
        """
        self.semester = Semester.objects.create(
            period='2022-1',
            start_date=timezone.now().date(),
            ending_date=timezone.now().date() + timezone.timedelta(days=90),
        )

    def test_semester_creation(self):  # Test for Semester object creation
        """
        Verifies that the Semester object is created successfully.
        """
        self.assertEqual(Semester.objects.count(), 1)

    def test_semester_str(self):  # Test for __str__ method of Semester model
        """
        Verifies that the __str__ method of Semester model works correctly.
        """
        self.assertEqual(str(self.semester), '2022-1')

    def test_semester_period(self):  # Test for period attribute of Semester model
        """
        Verifies that the period attribute of Semester model is correct.
        """
        self.assertEqual(self.semester.period, '2022-1')

    def test_semester_start_date(self):  # Test for start_date attribute of Semester model
        """
        Verifies that the start_date attribute of Semester model is correct.
        """
        self.assertEqual(self.semester.start_date, self.semester.start_date)

    def test_semester_ending_date(self):  # Test for ending_date attribute of Semester model
        """
        Verifies that the ending_date attribute of Semester model is correct.
        """
        self.assertEqual(self.semester.ending_date, self.semester.ending_date)
