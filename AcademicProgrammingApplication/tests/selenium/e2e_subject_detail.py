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

class SubjectDetailTest(StaticLiveServerTestCase):
    databases = {'default': 'test', 'test': 'test'}
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

    def test_subject_detail(self):
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
        # Open the subject detail page
        search_input = self.driver.find_element("id", 'floatingInputGrid')
        search_input.send_keys("global")
        search_input.submit()
        subject_element = self.driver.find_element(By.XPATH, "//td/a[contains(text(), 'Test Subject')]")
        subject_element.click()
        time.sleep(1)
        # Verify the information of the subject
        subject_name_element = self.driver.find_element(By.XPATH, "//h2[contains(text(), 'Materia - Test Subject')]")
        self.assertTrue(subject_name_element.is_displayed(), "El nombre de la materia no se muestra correctamente")

        subject_code_element = self.driver.find_element(By.XPATH, "//dd[contains(text(), '1')]")
        self.assertTrue(subject_code_element.is_displayed(), "El código de la materia no se muestra correctamente")

        subject_nrc_element = self.driver.find_element(By.XPATH, "//dd[contains(text(), '123456')]")
        self.assertTrue(subject_nrc_element.is_displayed(), "El NRC de la materia no se muestra correctamente")

        subject_credits_element = self.driver.find_element(By.XPATH, "//dd[contains(text(), '3')]")
        self.assertTrue(subject_credits_element.is_displayed(), "Los créditos de la materia no se muestra correctamente")

        subject_type_element = self.driver.find_element(By.XPATH, "//dd[contains(text(), 'CURRICULAR')]")
        self.assertTrue(subject_type_element.is_displayed(), "El tipo de la materia no se muestra correctamente")

        subject_syllabus_element = self.driver.find_element(By.XPATH, "//dd/a[contains(text(), 'syllabus_dNDyNLf.pdf')]")
        self.assertTrue(subject_syllabus_element.is_displayed(), "El syllabus de la materia no se muestra correctamente")

        subject_start_element = self.driver.find_element(By.XPATH, "//dd[contains(text(), 'April 28, 2024')]")
        self.assertTrue(subject_start_element.is_displayed(), "La fecha de inicio de la materia no se muestra correctamente")

        subject_ending_element = self.driver.find_element(By.XPATH, "//dd[contains(text(), 'July 27, 2024')]")
        self.assertTrue(subject_ending_element.is_displayed(), "La fecha de fin de la materia no se muestra correctamente")

        subject_modality_element = self.driver.find_element(By.XPATH, "//dd[contains(text(), 'PRESENCIAL')]")
        self.assertTrue(subject_modality_element.is_displayed(), "La modalidad de la materia no se muestra correctamente")

        subject_num_sessions_element = self.driver.find_element(By.XPATH, "//dd[contains(text(), '10')]")
        self.assertTrue(subject_num_sessions_element.is_displayed(), "El número de sesiones de la materia no se muestra correctamente")
        # Verify the classes of the subject
        class1_element = self.driver.find_element(By.XPATH, "//td/a[contains(text(), '1')]")
        self.assertTrue(class1_element.is_displayed(), "La clase de la materia no se muestra correctamente")
        
        class2_element = self.driver.find_element(By.XPATH, "//td/a[contains(text(), '1')]")
        self.assertTrue(class2_element.is_displayed(), "La clase de la materia no se muestra correctamente")
