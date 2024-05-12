import os
import re
import time
from unittest import TestCase

from django.test import override_settings
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from AcademicProgrammingApplication.models import User, PlanningProposal


class PlanningProposalE2ETest(StaticLiveServerTestCase):
    def setUp(self):
        super().setUp()
        self.driver = WebDriver()
        self.driver.implicitly_wait(10)

    def tearDown(self):
        self.driver.quit()
        super().tearDown()

    @override_settings(DEBUG=True)
    def test_upload_file(self):
        # Log in
        self.driver.get(self.live_server_url)
        username_input = self.driver.find_element("name", 'username')
        password_input = self.driver.find_element("name", 'password')
        username_input.send_keys('admin')
        password_input.send_keys('admin')
        submit_button = self.driver.find_element("id", 'access')
        submit_button.click()

        # Navigate to the page
        self.driver.get(self.live_server_url + '/planning_proposal')

        # Upload a file
        file_path = '../ccsa-grupo-1/test_file/info_de_Banner.xlsx'
        absolute_file_path = os.path.abspath(file_path)
        print(f'Ruta absoluta del archivo: {absolute_file_path}')

        file_input = self.driver.find_element("name", 'file')
        file_input.send_keys(absolute_file_path)

        # Click the update button
        update_button = self.driver.find_element("name", 'action')
        update_button.click()
        time.sleep(20)  # Espera suficiente para la actualización

        # Desplazarse hasta el final de la página
        self.scroll_to_bottom()

        # Click the download button
        download_button = self.driver.find_element("name", 'download-btn')
        download_button.click()

        # Esperar a que el archivo se descargue
        download_dir = "C:/Users/David/Downloads"
        file_pattern = r"Programacion_\d{2}-\d{2}-\d{4}_\d{6}\.xlsx"
        assert os.path.exists(download_dir), "El directorio de descargas no existe."

        WebDriverWait(self.driver, 30).until(
            lambda driver: any(re.match(file_pattern, f) for f in os.listdir(download_dir))
        )

        # Verificar la visibilidad y habilitación del botón de actualización
        #
        #print("is displayed update btn?: "+update_button.is_enabled())
        #self.assertTrue(update_button.is_enabled(), "El botón de actualización no está visible")
        #self.assertTrue(update_button.is_enabled(), "El botón de actualización no está habilitado")

        # Eliminar los archivos descargados
        downloaded_files = [f for f in os.listdir(download_dir) if re.match(file_pattern, f)]
        for file_name in downloaded_files:
            os.remove(os.path.join(download_dir, file_name))

    def scroll_to_bottom(self):
        # Obtener la altura de la página antes de desplazar
        last_height = self.driver.execute_script("return document.body.scrollHeight")

        # Desplazar hasta el final de la página
        while True:
            # Desplazar hacia abajo
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)  # Esperar un momento para que la página cargue contenido adicional

            # Calcular la nueva altura de la página después del desplazamiento
            new_height = self.driver.execute_script("return document.body.scrollHeight")

            # Si la altura de la página no ha cambiado, hemos llegado al final del contenido
            if new_height == last_height:
                break

            # Actualizar la altura de la página
            last_height = new_height
