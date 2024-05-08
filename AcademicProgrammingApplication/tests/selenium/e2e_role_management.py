import time
from selenium import webdriver
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.core.management import call_command
from selenium.webdriver.common.by import By

from AcademicProgrammingApplication.models import Role, User

class RolManagementTest(StaticLiveServerTestCase):
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
        # Find the radio button for "Líder de procesos" role for user Esteban
        users = self.driver.find_elements(By.CSS_SELECTOR, "table tbody tr")
        user_position = None
        for i, user in enumerate(users, start=1):
            username = user.find_element(By.CSS_SELECTOR, "td:nth-child(2)").text
            if username == "Esteban":
                user_position = i
                break
        if user_position is None:
            raise ValueError("User 'Esteban' not found")
        lider_role_radio_button = self.driver.find_element(By.CSS_SELECTOR, f"input[name='role{user_position}'][value='Líder de procesos']")
        # Click the radio button to change Esteban's role to "Líder de procesos"
        self.driver.execute_script("arguments[0].click();", lider_role_radio_button)
        # Find the save button and click it
        save_button = self.driver.find_element("id", "saveBtn")
        save_button.click()
        # Assert that the role has been changed
        updated_user = User.objects.get(username='Esteban')
        self.assertEqual(updated_user.role, self.role1)