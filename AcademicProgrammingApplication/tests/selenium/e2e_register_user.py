import time
from selenium import webdriver
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.core.management import call_command
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from AcademicProgrammingApplication.models import Role, User

class RolManagementRegisterUserTest(StaticLiveServerTestCase):
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
        # Go to the register user page
        self.driver.get(self.live_server_url + '/accounts/sign_up/')
        time.sleep(1)
        # Complete the data to register an user
        name_element = self.driver.find_element("id", 'username')
        name_element.send_keys("David47")

        first_name_element = self.driver.find_element("id", 'first_name')
        first_name_element.send_keys("David")

        last_name_element = self.driver.find_element("id", 'last_name')
        last_name_element.send_keys("Toronja")

        email_element = self.driver.find_element("id", 'email')
        email_element.send_keys("david@gmail.com")

        password1 = self.driver.find_element("name", 'password1')
        password1.send_keys("12345")

        password2 = self.driver.find_element("name", 'password2')
        password2.send_keys("12345")

        submit_button = self.driver.find_element("id", 'registrationButton')
        submit_button.click()
        # Verify that the user is created
        name_element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//td[contains(text(), 'David47')]"))
        )
        self.assertTrue(name_element.is_displayed())

        first_name_element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//td[contains(text(), 'David')]"))
        )
        self.assertTrue(first_name_element.is_displayed())

        last_name_element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//td[contains(text(), 'Toronja')]"))
        )
        self.assertTrue(last_name_element.is_displayed())

        email_element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//td[contains(text(), 'david@gmail.com')]"))
        )
        self.assertTrue(email_element.is_displayed())