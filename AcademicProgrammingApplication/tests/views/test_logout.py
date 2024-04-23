# Importing necessary modules
from django.test import TestCase, Client
from django.contrib.auth.models import User

class LogoutViewTest(TestCase):  # Defining a test case class for logout view
    def setUp(self):  # Setting up initial conditions for each test
        self.client = Client()  # Creating a test client
        self.test_user = User.objects.create_user(username='testuser', password='testpassword123')  # Creating a test user

    def test_logout_view(self):  # Test for logout view
        # Log in the user
        self.client.login(username='testuser', password='testpassword123')  # Logging in as the test user

        # Check that the user is logged in
        self.assertEqual(int(self.client.session['_auth_user_id']), self.test_user.pk)  # Checking if user is logged in

        # Log out the user
        response = self.client.get('/logout')  # Sending a GET request to logout

        # Check that the user is logged out
        self.assertNotIn('_auth_user_id', self.client.session)  # Checking if user is logged out

        # Check that the response is a redirect to the home page
        self.assertEqual(response.status_code, 302)  # Checking if response status code is 302 (redirect)
        self.assertEqual(response.url, '/')  # Checking if the response redirects to the home page URL