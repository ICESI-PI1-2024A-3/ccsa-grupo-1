from django.test import RequestFactory, TestCase
from AcademicProgrammingApplication.models import User
from AcademicProgrammingApplication.views import error_404

class Error404ViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='testuser', password='password')
        
    def test_error_404_rendering(self):
        # Create an HTTP request object
        request = self.factory.get('/some-url-that-does-not-exist/')
        request.user = self.user
        # Call the error_404 view with the request and capture the response
        response = error_404(request, None)
        # Verify that the response is successful (status code 404)
        self.assertEqual(response.status_code, 404)