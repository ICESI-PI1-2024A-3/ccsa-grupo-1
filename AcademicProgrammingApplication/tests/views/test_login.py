# Importing necessary modules and models
from django.test import TestCase, Client
from django.urls import reverse
from AcademicProgrammingApplication.models import User
from AcademicProgrammingApplication.forms import UserForm  # Importing UserForm from forms module


class LoginViewTest(TestCase):  # Defining a test case class for login view
    def setUp(self):  # Setting up initial conditions for each test
        self.client = Client()  # Creating a test client
        self.login_url = reverse('login')  # Getting the URL for login view
        self.user = User.objects.create_user(username='testuser', password='password')  # Creating a user

    def test_login_get(self):  # Test for GET request to login view
        response = self.client.get(self.login_url)  # Sending a GET request
        self.assertEqual(response.status_code, 200)  # Checking if response status code is 200
        self.assertTemplateUsed(response, 'login.html')  # Checking if 'login.html' template is used
        self.assertIsInstance(response.context['form'],
                              UserForm)  # Checking if the form instance in the context is UserForm

    def test_login_post_incorrect_credentials(self):  # Test for POST request with incorrect credentials
        response = self.client.post(self.login_url, {'username': 'testuser',
                                                     'password': 'wrongpassword'})  # Sending a POST request with incorrect credentials
        self.assertEqual(response.status_code, 200)  # Checking if response status code is 200
        self.assertTemplateUsed(response, 'login.html')  # Checking if 'login.html' template is used
        self.assertIsInstance(response.context['form'],
                              UserForm)  # Checking if the form instance in the context is UserForm
        self.assertIn('error', response.context)  # Checking if 'error' key exists in the context
        self.assertEqual(response.context['error'],
                         'Nombre de usuario o contraseña incorrectos.')  # Checking if the error message is correct

    def test_login_post_correct_credentials(self):  # Test for POST request with correct credentials
        response = self.client.post(self.login_url, {'username': 'testuser',
                                                     'password': 'password'})  # Sending a POST request with correct credentials
        self.assertRedirects(response, reverse('home'))  # Checking if the response redirects to 'home' URL
