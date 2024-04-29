import json
import time
from django.contrib.auth.models import User
from selenium import webdriver
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.core.management import call_command
from django.contrib.auth.hashers import make_password
from selenium.webdriver.common.by import By

from AcademicProgrammingApplication.models import Program, Semester, Subject

def create_user():
    username = 'admin'
    password = 'admin'
    user = User.objects.create(username=username, password=make_password(password))
    return user, password

class AcademicManagementTest(StaticLiveServerTestCase):
    databases = {'default': 'test', 'test': 'test'}
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user, cls.password = create_user()
        call_command('loaddata', 'test.json')
        with open('test.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
            program_data = next((item for item in data if item['model'] == 'AcademicProgrammingApplication.Program'), None)
            if program_data:
                program_pk = program_data['pk']
                program = Program.objects.get(pk=program_pk)
                semester_ids = program_data['fields']['semesters']
                semesters = Semester.objects.filter(period__in=semester_ids)
                program.semesters.set(semesters)
                subject_ids = program_data['fields']['subjects']
                subjects = Subject.objects.filter(pk__in=subject_ids)
                program.subjects.set(subjects)
                print(f"Programa: {program.name}")
                print(f"Semestres: {', '.join(str(semester) for semester in program.semesters.all())}")
                print(f"Materias: {', '.join(str(subject) for subject in program.subjects.all())}")


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
        # Find the search bar
        search_input = self.driver.find_element("id", 'floatingInputGrid')
        search_input.send_keys("Global")
        time.sleep(120)
