import os
import time
from unittest import TestCase
from venv import logger

from django.test import override_settings
from AcademicProgrammingApplication.models import User
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth.models import User
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from AcademicProgrammingApplication.models import PlanningProposal

    
class PlanningProposalTest(StaticLiveServerTestCase):
    def setUp(self):
        super().setUp()
        self.driver = WebDriver()
        self.driver.implicitly_wait(10)

    def tearDown(self):
        self.driver.quit()
        super().tearDown()

    @override_settings(DEBUG=True)
    def test_upload_file(self):
        # Log in
        self.driver.get(self.live_server_url)
        username_input = self.driver.find_element("name", 'username')
        password_input = self.driver.find_element("name", 'password')
        username_input.send_keys('admin')
        password_input.send_keys('admin')
        submit_button = self.driver.find_element("id", 'access')
        submit_button.click()

        # Upload a file

        # Navigate to the page
        self.driver.get(self.live_server_url + '/planning_proposal')
        file_path = '../ccsa-grupo-1/media/uploads/info_de_Banner.xlsx'
        absolute_file_path = os.path.abspath(file_path)
        print(f'Ruta absoluta del archivo: {absolute_file_path}')

        file_input = self.driver.find_element("name", 'file')
        file_input.send_keys(absolute_file_path)

        # Check if the update button is displayed and enabled
        update_button = self.driver.find_element("name", 'action')
        self.assertTrue(update_button.is_displayed(), "El botón de actualización no está visible")
        self.assertTrue(update_button.is_enabled(), "El botón de actualización no está habilitado")

        # Click the update button
        update_button.click()
        time.sleep(2)
