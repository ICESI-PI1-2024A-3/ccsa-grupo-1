from django.test import RequestFactory, TestCase  # Import necessary modules
from AcademicProgrammingApplication.models import User  # Import relevant model
from AcademicProgrammingApplication.views import error_404  # Import the view to be tested


class Error404ViewTestCase(TestCase):
    def setUp(self):
        """
        Set up initial conditions for the test.
        """
        self.factory = RequestFactory()  # Create a request factory object
        self.user = User.objects.create_user(username='testuser', password='password')  # Create a user

    def test_error_404_rendering(self):
        """
        Test the rendering of the 404 error page.
        """
        # Create an HTTP request object
        request = self.factory.get('/some-url-that-does-not-exist/')
        request.user = self.user  # Assign a user to the request (optional)
        # Call the error_404 view with the request and capture the response
        response = error_404(request, None)
        # Verify that the response status code is 404
        self.assertEqual(response.status_code, 404)
