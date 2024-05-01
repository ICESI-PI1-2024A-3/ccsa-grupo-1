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

class EditClassTest(StaticLiveServerTestCase):
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
        subject_link = self.driver.find_element(By.XPATH, "//td/a[contains(text(), 'Test Subject')]")
        subject_link.click()
        time.sleep(1)
        # Go to the class page
        class_link = self.driver.find_element(By.LINK_TEXT, "1")
        class_link.click()
        time.sleep(1)
        # Verify the information of the class
        class_name_element = self.driver.find_element(By.XPATH, "//h2[contains(text(), 'Clase - Test Subject')]")
        self.assertTrue(class_name_element.is_displayed(), "El nombre de la clase no se muestra correctamente")

        class_code_element = self.driver.find_element(By.XPATH, "//div[contains(text(), '1')]")
        self.assertTrue(class_code_element.is_displayed(), "El código de la clase no se muestra correctamente")

        class_nrc_element = self.driver.find_element(By.XPATH, "//div[contains(text(), '123456')]")
        self.assertTrue(class_nrc_element.is_displayed(), "El NRC de la clase no se muestra correctamente")

        class_credits_element = self.driver.find_element(By.XPATH, "//div[contains(text(), '3')]")
        self.assertTrue(class_credits_element.is_displayed(), "Los créditos de la clase no se muestra correctamente")

        class_type_element = self.driver.find_element(By.XPATH, "//div[contains(text(), 'CURRICULAR')]")
        self.assertTrue(class_type_element.is_displayed(), "El tipo de la clase no se muestra correctamente")

        class_syllabus_element = self.driver.find_element(By.XPATH, "//div[contains(text(), 'syllabus_dNDyNLf.pdf')]")
        self.assertTrue(class_syllabus_element.is_displayed(), "El syllabus de la clase no se muestra correctamente")

        class_start_element = self.driver.find_element(By.XPATH, "//div[contains(text(), 'April 28, 2024, 1 p.m.')]")
        self.assertTrue(class_start_element.is_displayed(), "La fecha de inicio de la clase no se muestra correctamente")

        class_ending_element = self.driver.find_element(By.XPATH, "//div[contains(text(), 'April 28, 2024, 2 p.m.')]")
        self.assertTrue(class_ending_element.is_displayed(), "La fecha de fin de la clase no se muestra correctamente")

        class_teacher_element = self.driver.find_element(By.XPATH, "//div[contains(text(), 'Miguel Campos')]")
        self.assertTrue(class_teacher_element.is_displayed(), "El profesor de la clase no se muestra correctamente")

        class_modality_element = self.driver.find_element(By.XPATH, "//div[contains(text(), 'PRESENCIAL')]")
        self.assertTrue(class_modality_element.is_displayed(), "La modalidad de la clase no se muestra correctamente")

        class_classroom_element = self.driver.find_element(By.XPATH, "//div[contains(text(), 'Test Classroom')]")
        self.assertTrue(class_classroom_element.is_displayed(), "El salón de la clase no se muestra correctamente")