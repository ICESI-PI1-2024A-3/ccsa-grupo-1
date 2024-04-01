# Importing necessary modules
from django.test import TestCase, Client
from django.contrib.auth.models import User

class SignUpViewTest(TestCase):  # Defining a test case class for sign-up view
    def setUp(self):  # Setting up initial conditions for each test
        self.client = Client()  # Creating a test client

    def test_signup_view_get(self):  # Test for GET request to sign-up view
        response = self.client.get('/accounts/sign_up/')  # Sending a GET request to sign-up view
        self.assertEqual(response.status_code, 200)  # Checking if response status code is 200
        self.assertTemplateUsed(response, 'sign-up.html')  # Checking if 'sign-up.html' template is used

    def test_signup_view_post(self):  # Test for POST request to sign-up view
        response = self.client.post('/accounts/sign_up/', {  # Sending a POST request with form data
            'username': 'testuser',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
            'email': 'testuser@example.com',
            'rol': 'Administrador'
        })
        self.assertEqual(response.status_code, 302)  # Checking if response status code is 302 (Redirection to 'home')
        self.assertTrue(User.objects.filter(username='testuser').exists())  # Checking if the user is created successfully

    def test_signup_view_post_password_mismatch(self):  # Test for POST request with password mismatch
        response = self.client.post('/accounts/sign_up/', {  # Sending a POST request with password mismatch
            'username': 'testuser',
            'password1': 'testpassword123',
            'password2': 'wrongpassword123',
            'email': 'testuser@example.com',
            'rol': 'Administrador'
        })
        self.assertEqual(response.status_code, 200)  # Checking if response status code is 200 (Render the same page with error)
        self.assertContains(response, '¡Las contraseñas no coinciden!')  # Checking if error message is displayed in the response

    def test_signup_view_post_user_exists(self):  # Test for POST request with existing username
        User.objects.create_user(username='existinguser', password='testpassword123')  # Creating an existing user
        response = self.client.post('/accounts/sign_up/', {  # Sending a POST request with existing username
            'username': 'existinguser',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
            'email': 'testuser@example.com',
            'rol': 'Administrador'
        })
        self.assertEqual(response.status_code, 200)  # Checking if response status code is 200 (Render the same page with error)
        self.assertContains(response, '¡El usuario ya existe!')  # Checking if error message is displayed in the response