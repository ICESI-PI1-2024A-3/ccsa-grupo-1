import time
from selenium import webdriver
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.core.management import call_command
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TeacherManagementTest(StaticLiveServerTestCase):
    databases = {'default': 'test'}
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        call_command('loaddata', 'test.json', verbosity=0)
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

    def test_teacher_management(self):
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
        # Go to the teacheer page
        self.driver.get(self.live_server_url + '/teacher_management')
        time.sleep(1)
        # Search a teacher
        search_input = self.driver.find_element(By.ID, "search-input")
        search_input.send_keys("Miguel Campos")
        search_input.send_keys(Keys.RETURN)
        time.sleep(1)
        # Espera hasta que el elemento esté presente
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//td/a[contains(text(), 'Miguel Campos')]"))
        )
        # Verification
        search_result = self.driver.find_element(By.XPATH, "//td/a[contains(text(), 'Miguel Campos')]")
        self.assertTrue(search_result.is_displayed())