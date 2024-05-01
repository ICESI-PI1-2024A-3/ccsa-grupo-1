from selenium import webdriver
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.core.management import call_command
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class SubjectDetailTest(StaticLiveServerTestCase):
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

    def test_subject_detail(self):
        # Open the login page
        self.driver.get(self.live_server_url)
        # Enter credentials and submit the form
        username_input = self.driver.find_element("name", 'username')
        password_input = self.driver.find_element("name", 'password')
        username_input.send_keys('admin')
        password_input.send_keys('admin')
        submit_button = self.driver.find_element("id", 'access')
        submit_button.click()
        # Open the subject detail page
        search_input = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, 'floatingInputGrid'))
        )
        search_input.send_keys("global")
        search_input.submit()
        subject_element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//td/a[contains(text(), 'Test Subject')]"))
        )
        subject_element.click()
        # Verify the information of the subject
        subject_name_element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//h2[contains(text(), 'Materia - Test Subject')]"))
        )
        self.assertTrue(subject_name_element.is_displayed(), "El nombre de la materia no se muestra correctamente")

        subject_code_element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//dd[contains(text(), '1')]"))
        )
        self.assertTrue(subject_code_element.is_displayed(), "El código de la materia no se muestra correctamente")

        subject_nrc_element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//dd[contains(text(), '123456')]"))
        )
        self.assertTrue(subject_nrc_element.is_displayed(), "El NRC de la materia no se muestra correctamente")

        subject_credits_element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//dd[contains(text(), '3')]"))
        )
        self.assertTrue(subject_credits_element.is_displayed(), "Los créditos de la materia no se muestra correctamente")

        subject_type_element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//dd[contains(text(), 'CURRICULAR')]"))
        )
        self.assertTrue(subject_type_element.is_displayed(), "El tipo de la materia no se muestra correctamente")

        subject_syllabus_element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//dd/a[contains(text(), 'syllabus_dNDyNLf.pdf')]"))
        )
        self.assertTrue(subject_syllabus_element.is_displayed(), "El syllabus de la materia no se muestra correctamente")

        subject_start_element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//dd[contains(text(), 'April 28, 2024')]"))
        )
        self.assertTrue(subject_start_element.is_displayed(), "La fecha de inicio de la materia no se muestra correctamente")

        subject_ending_element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//dd[contains(text(), 'July 27, 2024')]"))
        )
        self.assertTrue(subject_ending_element.is_displayed(), "La fecha de fin de la materia no se muestra correctamente")

        subject_modality_element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//dd[contains(text(), 'PRESENCIAL')]"))
        )
        self.assertTrue(subject_modality_element.is_displayed(), "La modalidad de la materia no se muestra correctamente")

        subject_num_sessions_element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//dd[contains(text(), '10')]"))
        )
        self.assertTrue(subject_num_sessions_element.is_displayed(), "El número de sesiones de la materia no se muestra correctamente")