import os
import time
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from django.core.management import call_command
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class PlanningProposalTest(StaticLiveServerTestCase):
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

    def test_search(self):
        # Log in
        self.driver.get(self.live_server_url)
        username_input = self.driver.find_element("name", 'username')
        password_input = self.driver.find_element("name", 'password')
        username_input.send_keys('admin')
        password_input.send_keys('admin')
        submit_button = self.driver.find_element("id", 'access')
        submit_button.click()

        # Navigate to the page
        self.driver.get(self.live_server_url + '/planning_proposal')
        file_path = '../ccsa-grupo-1/test_file/info_de_Banner.xlsx'
        absolute_file_path = os.path.abspath(file_path)

        file_input = self.driver.find_element("name", 'file')
        file_input.send_keys(absolute_file_path)

        # Click the update button
        update_button = self.driver.find_element("name", 'action')
        update_button.click()
        time.sleep(1)

        # Search admin
        search_input = self.driver.find_element("name", 'search_query')
        search_input.clear()
        search_input.send_keys('David')
        search_input.submit()
        time.sleep(1)

        # Verifications
        teacher_element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//td[contains(text(), 'Ana Carolina Martinez Romero')]"))
        )
        self.assertTrue(teacher_element.is_displayed())

        subject_element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//td[contains(text(), 'Creación de empresa: de la idea a la implementación')]"))
        )
        self.assertTrue(subject_element.is_displayed())

        date_element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//td[contains(text(), '15 de marzo de 2024 a las 00:00')]"))
        )
        self.assertTrue(date_element.is_displayed())

        editor_element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//td[contains(text(), 'David')]"))
        )
        self.assertTrue(editor_element.is_displayed())

        comment_element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//td[contains(text(), 'Cancelado por inundacion en la Universidad')]"))
        )
        self.assertTrue(comment_element.is_displayed())
        