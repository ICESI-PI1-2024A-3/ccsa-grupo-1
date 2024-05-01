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

class AcademicManagementTest(StaticLiveServerTestCase):
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
        search_input.send_keys("global")
        search_input.submit()
        time.sleep(1)
        # Verify the information of the postgraduate
        program_name_element = self.driver.find_element(By.XPATH, "//div[contains(text(), 'Global MBA')]")
        self.assertTrue(program_name_element.is_displayed(), "El nombre del programa no se muestra correctamente")

        program_type_element = self.driver.find_element(By.XPATH, "//div[contains(text(), 'ESPECIALIZACIÓN')]")
        self.assertTrue(program_type_element.is_displayed(), "El tipo del programa no se muestra correctamente")

        program_faculty_element = self.driver.find_element(By.XPATH, "//div[contains(text(), 'Facultad de Ciencias Administrativas y Económicas')]")
        self.assertTrue(program_faculty_element.is_displayed(), "La facultad del programa no se muestra correctamente")

        program_modality_element = self.driver.find_element(By.XPATH, "//div[contains(text(), 'VIRTUAL')]")
        self.assertTrue(program_modality_element.is_displayed(), "La modalidad del programa no se muestra correctamente")

        program_director_element = self.driver.find_element(By.XPATH, "//div[contains(text(), 'Nicholas Murray')]")
        self.assertTrue(program_director_element.is_displayed(), "El director del programa no se muestra correctamente")

        program_duration_element = self.driver.find_element(By.XPATH, "//div[contains(text(), '3 semestres')]")
        self.assertTrue(program_duration_element.is_displayed(), "La duración del programa no se muestra correctamente")

        program_cost_element = self.driver.find_element(By.XPATH, "//div[contains(text(), '25066618.00')]")
        self.assertTrue(program_cost_element.is_displayed(), "El costo del programa no se muestra correctamente")

        program_curriculum_element = self.driver.find_element(By.XPATH, "//div/a[contains(text(), 'curriculum_F8IwAuZ.pdf')]")
        self.assertTrue(program_curriculum_element.is_displayed(), "La malla curricular del programa no se muestra correctamente")
        # Verify the information of the semester
        semester_start_element = self.driver.find_element(By.XPATH, "//div[contains(text(), 'Feb. 1, 2024')]")
        self.assertTrue(semester_start_element.is_displayed(), "El inicio del semester no se muestra correctamente")

        semester_ending_element = self.driver.find_element(By.XPATH, "//div[contains(text(), 'June 30, 2024')]")
        self.assertTrue(semester_ending_element.is_displayed(), "El final del semester no se muestra correctamente")