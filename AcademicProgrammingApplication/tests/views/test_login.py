# Importing necessary modules and models
from django.test import TestCase, Client  # Import necessary modules
from django.urls import reverse  # Import reverse function
from AcademicProgrammingApplication.models import User  # Import User model
from AcademicProgrammingApplication.forms import UserForm  # Import UserForm from forms module


class LoginViewTest(TestCase):  # Defining a test case class for the login view
    def setUp(self):  # Set up initial conditions for each test
        self.client = Client()  # Create a test client
        self.login_url = reverse('login')  # Get the URL for the login view
        self.user = User.objects.create_user(username='testuser', password='password')  # Create a user

    def test_login_get(self):  # Test for GET request to the login view
        # Send a GET request
        response = self.client.get(self.login_url)
        # Verify the response status code is 200
        self.assertEqual(response.status_code, 200)
        # Verify that the 'login.html' template is used
        self.assertTemplateUsed(response, 'login.html')
        # Verify that the form instance in the context is UserForm
        self.assertIsInstance(response.context['form'], UserForm)

    def test_login_post_incorrect_credentials(self):  # Test for POST request with incorrect credentials
        # Send a POST request with incorrect credentials
        response = self.client.post(self.login_url, {'username': 'testuser', 'password': 'wrongpassword'})
        # Verify the response status code is 200
        self.assertEqual(response.status_code, 200)
        # Verify that the 'login.html' template is used
        self.assertTemplateUsed(response, 'login.html')
        # Verify that the form instance in the context is UserForm
        self.assertIsInstance(response.context['form'], UserForm)
        # Verify that the 'error' key exists in the context
        self.assertIn('error', response.context)
        # Verify that the error message is correct
        self.assertEqual(response.context['error'], 'Nombre de usuario o contraseña incorrectos.')

    def test_login_post_correct_credentials(self):  # Test for POST request with correct credentials
        # Send a POST request with correct credentials
        response = self.client.post(self.login_url, {'username': 'testuser', 'password': 'password'})
        # Verify the response redirects to the 'home' URL
        self.assertRedirects(response, reverse('home'))
