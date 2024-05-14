# Importing necessary modules
from django.test import TestCase, Client  # Import necessary modules
from AcademicProgrammingApplication.models import User  # Import User model


class LogoutViewTest(TestCase):  # Defining a test case class for the logout view
    def setUp(self):  # Set up initial conditions for each test
        self.client = Client()  # Create a test client
        self.test_user = User.objects.create_user(username='testuser', password='testpassword123')  # Create a test user

    def test_logout_view(self):  # Test for the logout view
        # Log in the user
        self.client.login(username='testuser', password='testpassword123')  # Log in as the test user

        # Check that the user is logged in
        self.assertEqual(int(self.client.session['_auth_user_id']), self.test_user.pk)  # Check if the user is logged in

        # Log out the user
        response = self.client.get('/logout')  # Send a GET request to log out

        # Check that the user is logged out
        self.assertNotIn('_auth_user_id', self.client.session)  # Check if the user is logged out

        # Check that the response is a redirect to the home page
        self.assertEqual(response.status_code, 302)  # Check if the response status code is 302 (redirect)
        self.assertEqual(response.url, '/')  # Check if the response redirects to the home page URL
