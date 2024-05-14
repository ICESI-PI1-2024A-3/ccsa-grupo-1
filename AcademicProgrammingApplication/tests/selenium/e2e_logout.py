import time
from selenium import webdriver
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.core.management import call_command
from selenium.webdriver.common.by import By


class LogoutTest(StaticLiveServerTestCase):
    """
    Scenery:

    The user logs in, then clicks the logout link and verifies that the logout is successful and is redirected to the
    login page.
    """
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

    def test_logout(self):
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
        # Find the logout link and click it
        logout_link = self.driver.find_element(By.LINK_TEXT, 'Salir')
        logout_link.click()
        time.sleep(1)
        # Verify that the current URL is the login page
        current_url = self.driver.current_url
        expected_url = self.live_server_url + '/'
        self.assertEqual(current_url, expected_url)
