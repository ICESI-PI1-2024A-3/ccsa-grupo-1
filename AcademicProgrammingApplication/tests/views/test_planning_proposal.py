from io import BytesIO  # Import necessary modules
from django.test import TestCase, Client  # Import necessary modules
from django.urls import reverse  # Import necessary modules
from AcademicProgrammingApplication.models import User, PlanningProposal  # Import necessary models
from django.core.files.base import ContentFile  # Import necessary modules
import pandas as pd  # Import necessary modules
from datetime import datetime  # Import necessary modules


class PlanningProposalTest(TestCase):  # Define a test case class for PlanningProposal
    def setUp(self):  # Set up initial conditions for each test
        self.client = Client()  # Create a test client
        self.url = reverse('planning_proposal')  # Create a URL for the planning_proposal view
        self.user = User.objects.create_user('testuser', 'password')  # Create a test user
        self.client.force_login(self.user)  # Log in the test user
        test_file_data = pd.DataFrame({  # Create test file data
            'Nombre_Profesor': ['Profesor 1', 'Profesor 2'],
            'Fecha_Inicio': [datetime.now(), datetime.now()],
            'Usuario_que_notifica': ['admin', 'admin'],
            'Comentario': ['Comentario 1', 'Comentario 2'],
            'Nombre_Materia': ['Materia 1', 'Materia 2']
        })
        test_file = BytesIO()  # Create a test file object
        test_file_data.to_excel(test_file, index=False)  # Write test file data to the test file object
        test_file.seek(0)  # Move the cursor to the beginning of the file
        self.test_file = PlanningProposal.objects.create(  # Create a test PlanningProposal object
            username=self.user.username,
            name_file='info_de_Banner.xlsx',
            path=ContentFile(test_file.getvalue(), 'info_de_Banner.xlsx')
        )

    def test_get_request(self):  # Test GET request to planning_proposal view
        response = self.client.get(self.url)  # Send a GET request
        self.assertEqual(response.status_code, 200)  # Check if response status code is 200
        self.assertTemplateUsed(response, 'academic-programming-proposal.html')  # Check if correct template is used

    def test_post_request_with_file(self):  # Test POST request with file
        test_file_data = {  # Create test file data
            'Nombre_Profesor': ['Profesor 1', 'Profesor 2'],
            'Fecha_Inicio': [datetime.now(), datetime.now()],
            'Usuario_que_notifica': ['admin', 'admin'],
            'Comentario': ['Comentario 1', 'Comentario 2'],
            'Nombre_Materia': ['Materia 1', 'Materia 2']
        }
        test_df = pd.DataFrame(test_file_data)  # Create a DataFrame from test file data
        test_file = BytesIO()  # Create a test file object
        test_df.to_excel(test_file, index=False)  # Write test DataFrame to the test file object
        test_file.seek(0)  # Move the cursor to the beginning of the file
        response = self.client.post(self.url, {'file': test_file},
                                    format='multipart')  # Send a POST request with the test file
        self.assertEqual(response.status_code, 200)  # Check if response status code is 200
        self.assertTemplateUsed(response, 'academic-programming-proposal.html')  # Check if correct template is used
        self.assertIsNotNone(response.context['file_selected'])  # Check if 'file_selected' context variable is not None

    def test_post_request_without_file(self):  # Test POST request without file
        response = self.client.post(self.url, {})  # Send a POST request without a file
        self.assertEqual(response.status_code, 200)  # Check if response status code is 200
        self.assertTemplateUsed(response, 'academic-programming-proposal.html')  # Check if correct template is used
        self.assertNotEqual(len(response.context['file_selected']),
                            0)  # Check if 'file_selected' context variable is not empty

    def test_search_filter(self):  # Test search filter
        response = self.client.get(self.url,
                                   {'search_query': self.user.username})  # Send a GET request with search parameter
        self.assertEqual(response.status_code, 200)  # Check if response status code is 200
        self.assertTemplateUsed(response, 'academic-programming-proposal.html')  # Check if correct template is used
        file_selected = response.context['file_selected']  # Get 'file_selected' context variable
        for record in file_selected:  # Iterate over file_selected records
            self.assertEqual(record['Usuario_que_notifica'], self.user.username)  # Check if user matches search query
