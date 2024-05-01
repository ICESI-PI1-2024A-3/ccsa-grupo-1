import time
from django.contrib.auth.models import User
from selenium import webdriver
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.core.management import call_command
from django.contrib.auth.hashers import make_password
from selenium.webdriver.common.by import By

def create_user():
    username = 'admin'
    password = 'admin'
    user = User.objects.create(username=username, password=make_password(password))
    return user, password

class ErrorAcademicManagementTest(StaticLiveServerTestCase):
    databases = {'default': 'test'}
    @classmethod
    def setUpClass(cls): 
        super().setUpClass()
        cls.user, cls.password = create_user()
        call_command('loaddata', 'test.json')

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

    def setUp(self):
        super().setUp()
        self.driver = webdriver.Chrome()

    def tearDown(self):
        self.driver.quit()
        super().tearDown()

    def test_search_program(self):
        # Open the login page
        self.driver.get(self.live_server_url)
        # Enter credentials and submit the form
        username_input = self.driver.find_element("name", 'username')
        password_input = self.driver.find_element("name", 'password')
        username_input.send_keys(self.user.username)
        password_input.send_keys(self.password)
        submit_button = self.driver.find_element("id", 'access')
        submit_button.click()
        time.sleep(1)
        # Find the search bar
        search_input = self.driver.find_element("id", 'floatingInputGrid')
        search_input.send_keys("marketing")
        search_input.submit()
        time.sleep(1)
        # Verify that the alert is show
        alert = self.driver.find_element(By.CLASS_NAME, 'alert-primary')
        self.assertTrue(alert.is_displayed(), 'La alerta no se muestra correctamente')