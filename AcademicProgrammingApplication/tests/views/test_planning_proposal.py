from django.test import TestCase, Client
from django.urls import reverse
from AcademicProgrammingApplication.models import PlanningProposal
from io import BytesIO
import pandas as pd
from datetime import datetime


class PlanningProposalTest(TestCase):
    def setUp(self):
        # Create a test client
        self.client = Client()
        # Create a URL for the planning_proposal view
        self.url = reverse('planning_proposal')
        # Create a test file object
        self.test_file = PlanningProposal.objects.create(name_file='test.xlsx', path='path/to/test.xlsx')

    # def test_get_request(self):
    #     # Test GET request to planning_proposal view
    #     response = self.client.get(self.url)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'academic-programming-proposal.html')

    def test_post_request_with_file(self):
        # Create a test file
        test_file_data = {
            'Nombre_Profesor': ['Profesor 1', 'Profesor 2'],
            'Fecha_Inicio': [datetime.now(), datetime.now()],
            'Comentario': ['Comentario 1', 'Comentario 2'],
            'Nombre_Materia': ['Materia 1', 'Materia 2']
        }
        test_df = pd.DataFrame(test_file_data)
        test_file = BytesIO()
        test_df.to_excel(test_file, index=False)
        test_file.seek(0)

        # Create a POST request with the test file
        response = self.client.post(self.url, {'file': test_file}, format='multipart')

        # Check if the response is successful
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'academic-programming-proposal.html')
        # Check if the file_selected context variable is not None
        self.assertIsNotNone(response.context['file_selected'])

    # def test_post_request_without_file(self):
    #     # Create a POST request without a file
    #     response = self.client.post(self.url, {})
    #     # Check if the response is successful
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'academic-programming-proposal.html')
    #     # Check if the file_selected context variable is None
    #     self.assertIsNone(response.context['file_selected'])
