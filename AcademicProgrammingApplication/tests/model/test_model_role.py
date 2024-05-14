from django.test import TestCase
from AcademicProgrammingApplication.models import Role


class RoleModelTest(TestCase):
    def setUp(self):
        """
        Creates Role objects for testing.
        """
        self.administrator_role = Role.objects.create(name='Administradores')
        self.process_leader_role = Role.objects.create(name='Líderes de procesos')
        self.process_assistant_role = Role.objects.create(name='Asistentes de proceso')

    def test_role_creation(self):
        """
        Verifies that Role objects are created successfully.
        """
        self.assertEqual(Role.objects.count(), 6)

    def test_administrator_role_name(self):
        """
        Verifies the name of the administrator role.
        """
        self.assertEqual(self.administrator_role.name, 'Administradores')

    def test_process_leader_role_name(self):
        """
        Verifies the name of the process leader role.
        """
        self.assertEqual(self.process_leader_role.name, 'Líderes de procesos')

    def test_process_assistant_role_name(self):
        """
        Verifies the name of the process assistant role.
        """
        self.assertEqual(self.process_assistant_role.name, 'Asistentes de proceso')

    def test_role_str(self):
        """
        Verifies that the __str__ method of Role model works correctly.
        """
        self.assertEqual(str(self.administrator_role), 'Administradores')
        self.assertEqual(str(self.process_leader_role), 'Líderes de procesos')
        self.assertEqual(str(self.process_assistant_role), 'Asistentes de proceso')
