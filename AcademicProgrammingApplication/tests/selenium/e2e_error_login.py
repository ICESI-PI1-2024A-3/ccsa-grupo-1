import time
from selenium import webdriver
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.core.management import call_command

class ErrorLoginTest(StaticLiveServerTestCase):
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
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()

    def tearDown(self):
        self.driver.quit()
        super().tearDown()

    def test_login_error(self):
        # Open the login page
        self.driver.get(self.live_server_url)
        # Find username and password input fields and submit button
        username_input = self.driver.find_element("name", 'username')
        password_input = self.driver.find_element("name", 'password')
        submit_button = self.driver.find_element("id", 'access')
        # Enter invalid username and password
        username_input.send_keys('invalidusername')
        password_input.send_keys('invalidpassword')
        # Click the submit button
        submit_button.click()
        # Wait for a brief moment for the error message to appear
        time.sleep(1)
        # Find the error message element
        login_error = self.driver.find_element("id", 'login-error')
        # Assert that the error message is displayed
        self.assertTrue(login_error.is_displayed(), 'Nombre de usuario o contraseña incorrectos.')