import time
from selenium import webdriver
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.core.management import call_command
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from AcademicProgrammingApplication.models import Role, User

class RolManagementErrorSearchUserTest(StaticLiveServerTestCase):
    databases = {'default': 'test'}
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        call_command('loaddata', 'test.json')
        call_command('loaddata', 'permissions.json')

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

    def setUp(self):
        super().setUp()
        self.role1 = Role.objects.get(name='Líder de procesos')
        self.role2 = Role.objects.get(name='Asistente de procesos')
        self.user1 = User.objects.create_user(username='Juan', password='12345', role=self.role1, email='juan@gmail.com')
        self.user2 = User.objects.create_user(username='Esteban', password='12345', role=self.role2, email='esteban@gmail.com')
        self.user3 = User.objects.create_user(username='Carlos', password='12345', role=self.role1, email='carlos@gmail.com')
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()

    def tearDown(self):
        self.driver.quit()
        super().tearDown()

    def test_role_management(self):
        # Open the login page
        self.driver.get(self.live_server_url)
        # Enter credentials and submit the form
        username_input = self.driver.find_element("name", 'username')
        password_input = self.driver.find_element("name", 'password')
        username_input.send_keys('admin')
        password_input.send_keys('admin')
        submit_button = self.driver.find_element("id", 'access')
        submit_button.click()
        time.sleep(1)
        # Go to the role management page
        self.driver.get(self.live_server_url + '/role_management')
        time.sleep(1)
        # Find the search bar
        search_input = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.NAME, 'user_search_engine'))
        )
        search_input.send_keys("notUser")
        search_input.submit()
        # Verify the searched results
        time.sleep(1)
        alert = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "alert-primary"))
        )
        self.assertTrue(alert.is_displayed(), 'La alerta no se muestra correctamente')
