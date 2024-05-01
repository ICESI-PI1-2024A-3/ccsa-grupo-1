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

class AssignTeacherTest(StaticLiveServerTestCase):
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
        
    def test_assign_teacher(self):
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
        # Open the assign teacher page
        current_url = self.driver.current_url
        base_url = current_url[:current_url.rfind('/')]
        edit_class_url = base_url + '/edit_class/3/'
        self.driver.get(edit_class_url)
        time.sleep(1)
        # Find the button for go to the assign teacher page
        assign_link = self.driver.find_element(By.CLASS_NAME, 'button-professor')
        assign_link.click()
        time.sleep(1)
        # Search a teacher
        search_input = self.driver.find_element("name", 'search')
        search_input.send_keys('miguel')
        search_button = self.driver.find_element("id", 'search-btn')
        search_button.click()
        time.sleep(1)
        # Save the class in the teacher
        save_button = self.driver.find_element(By.CLASS_NAME, 'btn-primary')
        save_button.click()
        time.sleep(1)
        # Verify the change of teacher in the class
        teacher_name_element = self.driver.find_element(By.XPATH, "//div[contains(text(), 'Miguel Campos')]")
        self.assertTrue(teacher_name_element.is_displayed(), "El nombre del profesor no se muestra correctamente")