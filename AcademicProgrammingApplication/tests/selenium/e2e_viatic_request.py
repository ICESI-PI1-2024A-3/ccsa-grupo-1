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

class ViaticRequestTest(StaticLiveServerTestCase):
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

    def test_viatic_request(self):

        self.driver.get(self.live_server_url + '/')
        username_input = self.driver.find_element(By.NAME, 'username')
        password_input = self.driver.find_element(By.NAME, 'password')
        username_input.send_keys(self.user.username)
        password_input.send_keys(self.password)
        submit_button = self.driver.find_element(By.ID, 'access')
        submit_button.click()
        time.sleep(1)

        self.driver.get(self.live_server_url + '/teacher/1/')

        solicitar_viatico_button = self.driver.find_element(By.ID, 'solicitar-viatico-btn')
        solicitar_viatico_button.click()
        time.sleep(1)

        tiquetes_select = self.driver.find_element(By.ID, 'tiquetes-select')
        tiquetes_select.send_keys("Si")
        hotel_select = self.driver.find_element(By.ID, 'hotel-select')
        hotel_select.send_keys("No")
        viatico_select = self.driver.find_element(By.ID, 'viatico-select')
        viatico_select.send_keys("Si")

        aceptar_button = self.driver.find_element(By.XPATH, "//button[text()='Aceptar']")
        aceptar_button.click()
        time.sleep(1)

        success_message = self.driver.find_element(By.CSS_SELECTOR, '.swal2-title').text
        self.assertEqual(success_message, 'Éxito')