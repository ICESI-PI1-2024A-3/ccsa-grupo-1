from selenium import webdriver
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.core.management import call_command
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class EditClassTest(StaticLiveServerTestCase):
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
        
        # Go to the class page
        current_url = self.driver.current_url
        base_url = current_url[:current_url.rfind('/')]
        edit_class_url = base_url + '/edit_class/1/'
        self.driver.get(edit_class_url)
        
        # Verify the information of the class
        class_name_element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//h2[contains(text(), 'Clase - Test Subject')]"))
        )
        self.assertTrue(class_name_element.is_displayed(), "El nombre de la clase no se muestra correctamente")

        class_code_element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(text(), '1')]"))
        )
        self.assertTrue(class_code_element.is_displayed(), "El código de la clase no se muestra correctamente")

        class_nrc_element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(text(), '123456')]"))
        )
        self.assertTrue(class_nrc_element.is_displayed(), "El NRC de la clase no se muestra correctamente")

        class_credits_element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(text(), '3')]"))
        )
        self.assertTrue(class_credits_element.is_displayed(), "Los créditos de la clase no se muestra correctamente")

        class_type_element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'CURRICULAR')]"))
        )
        self.assertTrue(class_type_element.is_displayed(), "El tipo de la clase no se muestra correctamente")

        class_syllabus_element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'syllabus_dNDyNLf.pdf')]"))
        )
        self.assertTrue(class_syllabus_element.is_displayed(), "El syllabus de la clase no se muestra correctamente")

        # Modificar la fecha de inicio
        start_date_button = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "start_date_class"))
        )
        start_date_button.click()
        datetime_input = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "datetime1"))
        )
        datetime_input.clear()
        datetime_input.send_keys('2024-05-01T13:00:00Z')
        submit_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[text()='Aceptar']"))
        )
        submit_button.click()

        # Modificar la fecha de fin
        end_date_button = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "end_date_class"))
        )
        end_date_button.click()
        datetime_input = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "datetime1"))
        )
        datetime_input.clear()
        datetime_input.send_keys('2024-05-01T14:00:00Z')
        submit_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[text()='Aceptar']"))
        )
        submit_button.click()

        # Esperar antes de hacer clic en el botón de aceptar
        # Esto le da tiempo a la ventana emergente para cargar completamente
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[text()='Aceptar']"))
        ).click()

        # Esperar a que la ventana emergente desaparezca
        WebDriverWait(self.driver, 10).until_not(
            EC.presence_of_element_located((By.CLASS_NAME, "swal2-container"))
        )

        # Modificar la modalidad
        modality_select = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, "tipoClase"))
        )
        modality_select.click()
        modality_option = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//option[text()='Clase virtual']"))  # Nueva modalidad
        )
        modality_option.click()

        

    