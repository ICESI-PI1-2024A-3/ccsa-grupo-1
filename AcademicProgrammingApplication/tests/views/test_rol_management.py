from django.test import TestCase, RequestFactory
from django.contrib.auth.models import Group, Permission
from AcademicProgrammingApplication.models import User, Role

class RoleManagementTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='testuser', password='12345', is_superuser=True
        )
        self.role1 = Role.objects.get(name='Líder de procesos')
        self.role2 = Role.objects.get(name='Asistente de procesos')
        self.user1 = User.objects.create_user(
            username='user1', password='password1', role=self.role1
        )
        self.user2 = User.objects.create_user(
            username='user2', password='password2', role=self.role2
        )
        permission = Permission.objects.get(codename='change_role')
        self.user.user_permissions.add(permission)

    def test_role_management_post(self):
        request = self.factory.post(
            '/role_management',
            data={
                'role1': 'Asistente de procesos',
                'role2': 'Líder de procesos',
            },
        )
        request.user = self.user
        from AcademicProgrammingApplication.views import role_management
        response = role_management(request)

        self.user1.refresh_from_db()
        self.user2.refresh_from_db()

        self.assertEqual(self.user1.role.name, 'Asistente de procesos')
        self.assertEqual(self.user2.role.name, 'Líder de procesos')

        user1_group = Group.objects.get(name='Asistente de procesos')
        user2_group = Group.objects.get(name='Líder de procesos')

        self.assertIn(user1_group, self.user1.groups.all())
        self.assertIn(user2_group, self.user2.groups.all())