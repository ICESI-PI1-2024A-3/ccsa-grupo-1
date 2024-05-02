from django.test import TestCase
from AcademicProgrammingApplication.models import Role

class RoleModelTest(TestCase):
    def setUp(self):
        self.administrator_role = Role.objects.create(name='Administradores')
        self.process_leader_role = Role.objects.create(name='Líderes de procesos')
        self.process_assistant_role = Role.objects.create(name='Asistentes de proceso')

    def test_role_creation(self):
        self.assertEqual(Role.objects.count(), 6)

    def test_administrator_role_name(self):
        self.assertEqual(self.administrator_role.name, 'Administradores')

    def test_process_leader_role_name(self):
        self.assertEqual(self.process_leader_role.name, 'Líderes de procesos')

    def test_process_assistant_role_name(self):
        self.assertEqual(self.process_assistant_role.name, 'Asistentes de proceso')

    def test_role_str(self):
        self.assertEqual(str(self.administrator_role), 'Administradores')
        self.assertEqual(str(self.process_leader_role), 'Líderes de procesos')
        self.assertEqual(str(self.process_assistant_role), 'Asistentes de proceso')