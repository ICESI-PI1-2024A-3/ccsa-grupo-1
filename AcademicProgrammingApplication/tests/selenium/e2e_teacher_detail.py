import time
from django.contrib.auth.models import User
from selenium import webdriver
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.core.management import call_command
from django.contrib.auth.hashers import make_password
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

def create_user():
    username = 'admin'
    password = 'admin'
    user = User.objects.create(username=username, password=make_password(password))
    return user, password

class TeacherDeatilTest(StaticLiveServerTestCase):
    databases = {'default': 'test', 'test': 'test'}
    
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user, cls.password = create_user()
        call_command('loaddata', 'test.json', verbosity=0)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

    def setUp(self):
        super().setUp()
        self.driver = webdriver.Chrome()

    def tearDown(self):
        self.driver.quit()
        super().tearDown()

    def test_teacher_management_and_detail(self):
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
        # Navegate to the teachers page
        self.driver.get(self.live_server_url + '/teacher_management')
        time.sleep(1)
        # Search a teacher
        search_input = self.driver.find_element(By.ID, "search-input")
        search_input.send_keys("Miguel Campos")
        search_input.send_keys(Keys.RETURN)
        time.sleep(1)
        # Go to the teacher information page
        teacher_link = self.driver.find_element(By.LINK_TEXT, "Miguel Campos")
        teacher_link.click()
        time.sleep(1)
        # Verifications
        self.assertIn("teacher", self.driver.current_url)

        teacher_name_element = self.driver.find_element(By.XPATH, "//dd[contains(text(), 'Miguel Campos')]")
        self.assertTrue(teacher_name_element.is_displayed(), "El nombre del profesor no se muestra correctamente")

        teacher_email_element = self.driver.find_element(By.XPATH, "//dd[contains(text(), 'test1@example.com')]")
        self.assertTrue(teacher_email_element.is_displayed(), "El email del profesor no se muestra correctamente")

        teacher_cellphone_element = self.driver.find_element(By.XPATH, "//dd[contains(text(), '123456789')]")
        self.assertTrue(teacher_cellphone_element.is_displayed(), "El número de celular del profesor no se muestra correctamente")

        teacher_city_element = self.driver.find_element(By.XPATH, "//dd[contains(text(), 'Test City')]")
        self.assertTrue(teacher_city_element.is_displayed(), "La ciudad del profesor no se muestra correctamente")

        teacher_state_element = self.driver.find_element(By.XPATH, "//dd[contains(text(), 'ACTIVO')]")
        self.assertTrue(teacher_state_element.is_displayed(), "El estado del profesor no se muestra correctamente")