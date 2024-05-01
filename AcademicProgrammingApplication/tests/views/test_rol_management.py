from django.test import TestCase, RequestFactory
from django.contrib.auth.models import AnonymousUser, Permission
from AcademicProgrammingApplication.models import User, Role
from AcademicProgrammingApplication.views import role_management

class RoleManagementTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.role = Role.objects.create(name='TestRole')
        self.user.role = self.role
        self.user.save()

        permission = Permission.objects.get(codename='change_role')
        self.user.user_permissions.add(permission)

    def test_role_management(self):
        request = self.factory.get('/role_management')
        request.user = self.user

        response = role_management(request)

        self.assertEqual(response.status_code, 200)

        self.assertContains(response, 'testuser')
        self.assertContains(response, 'TestRole')