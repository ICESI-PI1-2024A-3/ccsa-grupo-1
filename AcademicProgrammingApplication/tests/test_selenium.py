from django.test import TestCase
from selenium import webdriver

class MySeleniumTests(TestCase):
    def setUp(self):
        self.browser = webdriver.Chrome() # Initializes Chrome webdriver before each test

    def tearDown(self):
        self.browser.quit() # Closes the browser after each test

    def test_example(self):
        self.browser.get('http://127.0.0.1:8000/') # Opens the URL in the browser
        self.assertIn('Login', self.browser.title) # Asserts if 'Login' is present in the title of the page