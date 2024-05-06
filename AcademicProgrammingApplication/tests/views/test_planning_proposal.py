from io import BytesIO
from django.test import TestCase, Client
from django.urls import reverse
from AcademicProgrammingApplication.models import User, PlanningProposal
from django.core.files.base import ContentFile
import pandas as pd
from datetime import datetime

class PlanningProposalTest(TestCase):
    def setUp(self):
        # Create a test client to simulate web requests
        self.client = Client()
        # Create a URL for the planning_proposal view using its name
        self.url = reverse('planning_proposal')
        # Create a test user and log them in
        self.user = User.objects.create_user('testuser', 'password')
        self.client.force_login(self.user)
        # Create a test file object and associate it with the test user
        test_file_data = pd.DataFrame({
            'Nombre_Profesor': ['Profesor 1', 'Profesor 2'],
            'Fecha_Inicio': [datetime.now(), datetime.now()],
            'Usuario_que_notifica': ['admin', 'admin'],
            'Comentario': ['Comentario 1', 'Comentario 2'],
            'Nombre_Materia': ['Materia 1', 'Materia 2']
        })
        test_file = BytesIO()
        test_file_data.to_excel(test_file, index=False)
        test_file.seek(0)
        self.test_file = PlanningProposal.objects.create(
            username=self.user.username,
            name_file='info_de_Banner.xlsx',
            path=ContentFile(test_file.getvalue(), 'info_de_Banner.xlsx')
        )

    def test_get_request(self):
        # Test GET request to planning_proposal view
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'academic-programming-proposal.html')

    def test_post_request_with_file(self):
        # Create a test file with data
        test_file_data = {
            'Nombre_Profesor': ['Profesor 1', 'Profesor 2'],
            'Fecha_Inicio': [datetime.now(), datetime.now()],
            'Usuario_que_notifica': ['admin', 'admin'],
            'Comentario': ['Comentario 1', 'Comentario 2'],
            'Nombre_Materia': ['Materia 1', 'Materia 2']
        }
        test_df = pd.DataFrame(test_file_data)
        test_file = BytesIO()
        test_df.to_excel(test_file, index=False)
        test_file.seek(0)
        # Create a POST request with the test file
        response = self.client.post(self.url, {'file': test_file}, format='multipart')
        # Check if the response is successful and the correct template was used
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'academic-programming-proposal.html')
        # Check if the file_selected context variable is not None
        self.assertIsNotNone(response.context['file_selected'])

    def test_post_request_without_file(self):
        # Create a POST request without a file
        response = self.client.post(self.url, {})
        # Check if the response is successful and the correct template was used
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'academic-programming-proposal.html')
        # Check if the file_selected context variable is not empty
        self.assertNotEqual(len(response.context['file_selected']), 0)

    def test_search_filter(self):
        # Perform a GET request with the search parameter for the test user
        response = self.client.get(self.url, {'search_query': self.user.username})
        # Verify that the status code is 200 and the correct template was used
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'academic-programming-proposal.html')
        # Verify that the 'file_selected' context contains only files from the test user
        file_selected = response.context['file_selected']
        for record in file_selected:
            self.assertEqual(record['Usuario_que_notifica'], self.user.username)
