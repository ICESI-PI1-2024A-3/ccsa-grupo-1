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

    def test_upload_file(self):
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
        time.sleep(10)

        # Verification of the contents of the file
        teacher1_element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//td[contains(text(), 'Javier Adolfo Aguirre Ramos')]"))
        )
        self.assertTrue(teacher1_element.is_displayed())

        subject1_element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//td[contains(text(), 'Diseño para la innovación social')]"))
        )
        self.assertTrue(subject1_element.is_displayed())

        date1_element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//td[contains(text(), '12 de enero de 2024 a las 00:00')]"))
        )
        self.assertTrue(date1_element.is_displayed())

        editor1_element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//td[contains(text(), 'admin')]"))
        )
        self.assertTrue(editor1_element.is_displayed())

        comment1_element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//td[contains(text(), 'La clase fue movida por cuestion de que el profesor no pudo llegar')]"))
        )
        self.assertTrue(comment1_element.is_displayed())

        teacher2_element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//td[contains(text(), 'Ana Carolina Martinez Romero')]"))
        )
        self.assertTrue(teacher2_element.is_displayed())

        subject2_element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//td[contains(text(), 'Creación de empresa: de la idea a la implementación')]"))
        )
        self.assertTrue(subject2_element.is_displayed())

        date2_element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//td[contains(text(), '1 de marzo de 2024 a las 00:00')]"))
        )
        self.assertTrue(date2_element.is_displayed())

        editor2_element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//td[contains(text(), 'admin')]"))
        )
        self.assertTrue(editor2_element.is_displayed())

        comment2_element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//td[contains(text(), 'El profesor no pudo dictar la clase y se dicto el dia siguiente')]"))
        )
        self.assertTrue(comment2_element.is_displayed())

        teacher3_element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//td[contains(text(), 'Ana Carolina Martinez Romero')]"))
        )
        self.assertTrue(teacher3_element.is_displayed())

        subject3_element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//td[contains(text(), 'Creación de empresa: de la idea a la implementación')]"))
        )
        self.assertTrue(subject3_element.is_displayed())

        date3_element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//td[contains(text(), '15 de marzo de 2024 a las 00:00')]"))
        )
        self.assertTrue(date3_element.is_displayed())

        editor3_element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//td[contains(text(), 'David')]"))
        )
        self.assertTrue(editor3_element.is_displayed())

        comment3_element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//td[contains(text(), 'Cancelado por inundacion en la Universidad')]"))
        )
        self.assertTrue(comment3_element.is_displayed())