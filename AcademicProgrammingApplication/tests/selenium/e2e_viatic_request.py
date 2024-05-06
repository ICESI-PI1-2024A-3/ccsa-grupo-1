import time
from selenium import webdriver
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.core.management import call_command
from selenium.webdriver.common.by import By

class ViaticRequestTest(StaticLiveServerTestCase):
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

    def test_viatic_request(self):
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
        # Go to the teacher information page
        self.driver.get(self.live_server_url + '/teacher/1/')
        time.sleep(1)
        # Request a viatic
        request_viatic_button = self.driver.find_element(By.ID, 'solicitar-viatico-btn')
        request_viatic_button.click()
        time.sleep(1)
        tiquetes_select = self.driver.find_element(By.ID, 'tiquetes-select')
        tiquetes_select.send_keys("Si")
        hotel_select = self.driver.find_element(By.ID, 'hotel-select')
        hotel_select.send_keys("No")
        viatico_select = self.driver.find_element(By.ID, 'viatico-select')
        viatico_select.send_keys("Si")
        accept_button = self.driver.find_element(By.XPATH, "//button[text()='Aceptar']")
        accept_button.click()
        time.sleep(1)
        # Verification
        success_message = self.driver.find_element(By.CSS_SELECTOR, '.swal2-title').text
        self.assertEqual(success_message, 'Éxito')