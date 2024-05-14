from selenium import webdriver
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.core.management import call_command
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class AcademicManagementEditionTest(StaticLiveServerTestCase):
    """
    Scenery:

    The administrator user logs in, searches for an existing academic program, accesses the edit page, modifies the
    program details, and saves the changes. Then, verify that the updated details are displayed correctly in search.
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

    def test_edit_program(self):
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
        # Find the button for go to the edition page
        edition_link = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'btn-secondary'))
        )
        edition_link.click()
        # Change the information
        name_element = self.driver.find_element("id", 'name')
        name_element.clear()
        name_element.send_keys("Master en negocios")

        faculty_element = self.driver.find_element("id", 'faculty')
        faculty_element.clear()
        faculty_element.send_keys("Facultad de negocios")

        director_element = self.driver.find_element("id", 'program_manager')
        director_element.clear()
        director_element.send_keys("Juan Esteban Arango")

        cost_element = self.driver.find_element("name", 'cost')
        cost_element.clear()
        cost_element.send_keys("20000.00")

        type_select = self.driver.find_element(By.CSS_SELECTOR, 'select[name="type"]')
        type_options = self.driver.find_elements(By.CSS_SELECTOR, 'select[name="type"] option')
        new_type = type_options[1].text
        type_options[1].click()

        modality_select = self.driver.find_element(By.ID, 'modality')
        modality_options = self.driver.find_elements(By.CSS_SELECTOR, 'select[name="modality"] option')
        new_modality = modality_options[1].text
        modality_options[1].click()

        duration_element = self.driver.find_element("name", 'duration')
        duration_element.clear()
        duration_element.send_keys("10")

        submit_button = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, 'editButton'))
        )
        submit_button.click()
        # Verify the information of the postgraduate program
        search_input = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, 'floatingInputGrid'))
        )
        search_input.clear()
        search_input.send_keys("master en negocios")
        search_input.submit()

        program_name_element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'Master en negocios')]"))
        )
        self.assertTrue(program_name_element.is_displayed(), "El nombre del programa no se muestra correctamente")

        program_type_element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'MAESTRÍA')]"))
        )
        self.assertTrue(program_type_element.is_displayed(), "El tipo del programa no se muestra correctamente")

        program_faculty_element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'Facultad de negocios')]"))
        )
        self.assertTrue(program_faculty_element.is_displayed(), "La facultad del programa no se muestra correctamente")

        program_modality_element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'PRESENCIAL')]"))
        )
        self.assertTrue(program_modality_element.is_displayed(),
                        "La modalidad del programa no se muestra correctamente")

        program_director_element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'Juan Esteban Arango')]"))
        )
        self.assertTrue(program_director_element.is_displayed(), "El director del programa no se muestra correctamente")

        program_duration_element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(text(), '10 semestres')]"))
        )
        self.assertTrue(program_duration_element.is_displayed(), "La duración del programa no se muestra correctamente")

        program_cost_element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(text(), '20000,00')]"))
        )
        self.assertTrue(program_cost_element.is_displayed(), "El costo del programa no se muestra correctamente")

        program_curriculum_element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div/a[contains(text(), 'curriculum_F8IwAuZ.pdf')]"))
        )
        self.assertTrue(program_curriculum_element.is_displayed(),
                        "La malla curricular del programa no se muestra correctamente")
