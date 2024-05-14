from django.test import TestCase, Client  # Importing necessary modules
from django.urls import reverse  # Importing reverse function to generate URLs
from django.utils import timezone  # Importing timezone module
from AcademicProgrammingApplication.models import User, Semester, Program  # Importing relevant models


class AcademicManagementTest(TestCase):  # Defining a test case class

    def setUp(self):  # Setting up initial conditions for each test
        """
        Creates a test client, a superuser, and necessary objects for testing academic management.
        """
        self.client = Client()  # Creating a test client
        self.user = User.objects.create_superuser(username='user', password='pass')  # Creating a superuser
        self.client.login(username='user', password='pass')  # Logging in as the created user

        start_date = timezone.now()  # Getting current time
        ending_date = start_date + timezone.timedelta(days=90)  # Creating an ending date 90 days after start
        # Creating a semester
        self.semester = Semester.objects.create(period='2024-1', start_date=start_date,
                                                ending_date=ending_date)

        # Creating a program
        self.program = Program.objects.create(name='Programa de prueba', cost=1000, duration=4,
                                              faculty='Facultad de prueba', modality='Modalidad de prueba',
                                              type='Tipo de prueba', director='Director de prueba')

    def test_academic_management(self):  # Test case for academic management
        """
        Tests the home page for academic management.
        """
        response = self.client.get(reverse('home'), {'program': 'Programa de prueba', 'semester': '2024-1',
                                                     'subject_search': 'Asignatura de prueba'})
        self.assertEqual(response.status_code, 200)  # Checking if response status code is 200
        self.assertContains(response,
                            'Programa de prueba')  # Checking if 'Programa de prueba' is present in the response

    def test_delete_academic_program(self):  # Test case for deleting an academic program
        """
        Tests deleting an academic program.
        """
        response = self.client.get(reverse('delete_academic_program', args=[
            self.program.id]))  # Sending a GET request to delete an academic program
        self.assertEqual(response.status_code, 302)  # Checking if response status code is 302 (redirect)
        self.assertNotIn(self.program, Program.objects.all())  # Checking if the program is deleted

    def test_academic_program_edition(self):  # Test case for editing an academic program
        """
        Tests editing an academic program.
        """
        response = self.client.get(reverse('academic_program_edition',
                                           args=[self.program.id]))  # Sending a GET request to edit an academic program
        self.assertEqual(response.status_code, 200)  # Checking if response status code is 200
        self.assertContains(response,
                            'Programa de prueba')  # Checking if 'Programa de prueba' is present in the response

    def test_edit_academic_program(self):  # Test case for editing an academic program
        """
        Tests submitting a form to edit an academic program.
        """
        response = self.client.post(reverse('edit_academic_program', args=[self.program.id]),
                                    {  # Sending a POST request to edit an academic program
                                        'name': 'Nuevo nombre',
                                        'type': 'Nuevo tipo',
                                        'faculty': 'Nueva facultad',
                                        'modality': 'Nueva modalidad',
                                        'program_manager': 'Nuevo director',
                                        'duration': '5',
                                        'cost': '5000',
                                        # 'curriculum': 'Nuevo currículo'  # This field is a file

                                    })
        self.assertEqual(response.status_code, 302)  # Checking if response status code is 302 (redirects to home)
        self.program.refresh_from_db()  # Refreshing program from the database
        self.assertEqual(self.program.name, 'Nuevo nombre')  # Checking if the program name is updated
