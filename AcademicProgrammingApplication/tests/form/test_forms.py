from django.test import TestCase
from AcademicProgrammingApplication.forms import UserForm

class UserFormTest(TestCase):
    # Test case to check form validation with valid data
    def test_form_with_valid_data(self):
        # Create a form instance with valid data
        form = UserForm({
            'username': 'testuser',
            'password': 'testpassword123',
        })
        # Assert that the form is valid
        self.assertTrue(form.is_valid())

    # Test case to check form validation with invalid data
    def test_form_with_invalid_data(self):
        # Create a form instance with invalid data (empty username)
        form = UserForm({
            'username': '',
            'password': 'testpassword123',
        })
        # Assert that the form is not valid
        self.assertFalse(form.is_valid())