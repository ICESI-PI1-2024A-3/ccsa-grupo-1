from selenium import webdriver
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.core.management import call_command
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class ErrorAssignTeacherTest(StaticLiveServerTestCase):
    """
    Scenery:

    The user logs in, accesses the edit page for a specific class that already has a teacher assigned, navigates to
    the teacher assignment section, searches for a teacher, and verifies that a warning alert is displayed.
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

    def test_alert_assign_teacher(self):
        # Open the login page
        self.driver.get(self.live_server_url)
        # Enter credentials and submit the form
        username_input = self.driver.find_element("name", 'username')
        password_input = self.driver.find_element("name", 'password')
        username_input.send_keys('admin')
        password_input.send_keys('admin')
        submit_button = self.driver.find_element("id", 'access')
        submit_button.click()
        # Open the assign teacher page
        current_url = self.driver.current_url
        base_url = current_url[:current_url.rfind('/')]
        edit_class_url = base_url + '/edit_class/4/'
        self.driver.get(edit_class_url)
        # Find the button for go to the assign teacher page
        assign_link = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'button-professor'))
        )
        assign_link.click()
        # Search a teacher
        search_input = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.NAME, 'search'))
        )
        search_input.send_keys('miguel')
        search_button = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, 'search-btn'))
        )
        search_button.click()
        # Verify that the alert is show
        alert = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'alert-warning'))
        )
        self.assertTrue(alert.is_displayed(), 'La alerta no se muestra correctamente')
