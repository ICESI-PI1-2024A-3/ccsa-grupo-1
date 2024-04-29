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

class TeacherManagementTest(StaticLiveServerTestCase):
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

    def test_teacher_management(self):
        
        self.driver.get(self.live_server_url + '/')

        username_input = self.driver.find_element(By.NAME, 'username')

        password_input = self.driver.find_element(By.NAME, 'password')
        username_input.send_keys(self.user.username)
        password_input.send_keys(self.password)
        submit_button = self.driver.find_element(By.ID, 'access')
        submit_button.click()
        time.sleep(1)

        self.driver.get(self.live_server_url + '/teacher_management')

        search_input = self.driver.find_element(By.ID, "search-input")
        search_input.send_keys("Miguel Campos")
        search_input.send_keys(Keys.RETURN)