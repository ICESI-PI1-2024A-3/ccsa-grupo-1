from django.test import TestCase, RequestFactory  # Import necessary modules
from django.contrib.auth.models import Group, Permission  # Import necessary modules
from AcademicProgrammingApplication.models import User, Role  # Import necessary models


class RoleManagementTest(TestCase):  # Define a test case class for Role management
    def setUp(self):  # Set up initial conditions for each test
        self.factory = RequestFactory()  # Create a RequestFactory object
        self.user = User.objects.create_user(  # Create a test user
            username='testuser', password='12345', is_superuser=True
        )
        self.role1 = Role.objects.get(name='Líder de procesos')  # Get Role object for 'Líder de procesos'
        self.role2 = Role.objects.get(name='Asistente de procesos')  # Get Role object for 'Asistente de procesos'
        self.user1 = User.objects.create_user(  # Create a test user with 'Asistente de procesos' role
            username='user1', password='password1', role=self.role1
        )
        self.user2 = User.objects.create_user(  # Create a test user with 'Líder de procesos' role
            username='user2', password='password2', role=self.role2
        )
        permission = Permission.objects.get(codename='change_role')  # Get 'change_role' permission
        self.user.user_permissions.add(permission)  # Add 'change_role' permission to the test user

    def test_role_management_post(self):  # Test role management via POST request
        request = self.factory.post(  # Create a POST request
            '/role_management',
            data={
                'role1': 'Asistente de procesos',  # New role for user1
                'role2': 'Líder de procesos',  # New role for user2
            },
        )
        request.user = self.user  # Assign the test user to the request
        from AcademicProgrammingApplication.views import role_management  # Import the role_management view
        response = role_management(request)  # Call the role_management view with the request

        self.user1.refresh_from_db()  # Refresh user1 from the database
        self.user2.refresh_from_db()  # Refresh user2 from the database

        self.assertEqual(self.user1.role.name, 'Asistente de procesos')  # Check if user1's role is updated
        self.assertEqual(self.user2.role.name, 'Líder de procesos')  # Check if user2's role is updated

        user1_group = Group.objects.get(name='Asistente de procesos')  # Get Group object for 'Asistente de procesos'
        user2_group = Group.objects.get(name='Líder de procesos')  # Get Group object for 'Líder de procesos'

        self.assertIn(user1_group, self.user1.groups.all())  # Check if user1 is in the 'Asistente de procesos' group
        self.assertIn(user2_group, self.user2.groups.all())  # Check if user2 is in the 'Líder de procesos' group
