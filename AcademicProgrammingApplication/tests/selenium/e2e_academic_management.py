from selenium import webdriver
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.core.management import call_command
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class AcademicManagementTest(StaticLiveServerTestCase):
    databases = {'default': 'test'}
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        call_command('loaddata', 'test.json')

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

    def test_search_program(self):
        # Open the login page
        self.driver.get(self.live_server_url)
        # Enter credentials and submit the form
        username_input = self.driver.find_element("name", 'username')
        password_input = self.driver.find_element("name", 'password')
        username_input.send_keys('admin')
        password_input.send_keys('admin')
        submit_button = self.driver.find_element("id", 'access')
        submit_button.click()
        # Find the search bar
        search_input = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, 'floatingInputGrid'))
        )
        search_input.send_keys("global")
        search_input.submit()
        # Verify the information of the postgraduate program
        program_name_element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'Global MBA')]"))
        )
        self.assertTrue(program_name_element.is_displayed(), "El nombre del programa no se muestra correctamente")

        program_type_element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'ESPECIALIZACIÓN')]"))
        )
        self.assertTrue(program_type_element.is_displayed(), "El tipo del programa no se muestra correctamente")

        program_faculty_element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'Facultad de Ciencias Administrativas y Económicas')]"))
        )
        self.assertTrue(program_faculty_element.is_displayed(), "La facultad del programa no se muestra correctamente")

        program_modality_element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'VIRTUAL')]"))
        )
        self.assertTrue(program_modality_element.is_displayed(), "La modalidad del programa no se muestra correctamente")

        program_director_element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'Nicholas Murray')]"))
        )
        self.assertTrue(program_director_element.is_displayed(), "El director del programa no se muestra correctamente")

        program_duration_element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(text(), '3 semestres')]"))
        )
        self.assertTrue(program_duration_element.is_displayed(), "La duración del programa no se muestra correctamente")

        program_cost_element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(text(), '25066618.00')]"))
        )
        self.assertTrue(program_cost_element.is_displayed(), "El costo del programa no se muestra correctamente")

        program_curriculum_element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div/a[contains(text(), 'curriculum_F8IwAuZ.pdf')]"))
        )
        self.assertTrue(program_curriculum_element.is_displayed(), "La malla curricular del programa no se muestra correctamente")

        # Verify the information of the semester
        semester_start_element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'Feb. 1, 2024')]"))
        )
        self.assertTrue(semester_start_element.is_displayed(), "El inicio del semester no se muestra correctamente")

        semester_ending_element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'June 30, 2024')]"))
        )
        self.assertTrue(semester_ending_element.is_displayed(), "El final del semester no se muestra correctamente")