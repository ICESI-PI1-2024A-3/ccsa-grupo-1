from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from AcademicProgrammingApplication.models import Class, Subject
import json

class EditInfoClassTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='user', password='pass')
        self.client.login(username='user', password='pass')
        
        # Crear una materia de prueba
        self.subject = Subject.objects.create(name='Materia de Prueba', code='123')
        
        # Crear una clase de prueba asociada a la materia de prueba
        self.edit_class = Class.objects.create(id='001', subject=self.subject)
        
    def test_edit_info_class_view(self):
        # Acceder a la vista de edición de información de clase
        response = self.client.get(reverse('edit_info_class', args=[self.edit_class.id]))
        
        # Verificar que la respuesta sea exitosa
        self.assertEqual(response.status_code, 200)
        
        # Verificar que se muestra la información de la clase correctamente
        self.assertContains(response, 'Materia de Prueba')
        self.assertContains(response, '001')
        
    def test_edit_info_class_post_save(self):
        # Simular una solicitud POST para guardar cambios en la clase
        response = self.client.post(reverse('edit_info_class', args=[self.edit_class.id]), {'action': 'save'})
        
        # Verificar que se redirige correctamente después de guardar los cambios
        self.assertRedirects(response, reverse('subject_detail', args=[self.edit_class.subject.code]))
        
    def test_edit_info_class_post_cancel(self):
        # Simular una solicitud POST para cancelar cambios en la clase
        response = self.client.post(reverse('edit_info_class', args=[self.edit_class.id]), {'action': 'cancel'})
        
        # Verificar que se redirige correctamente después de cancelar los cambios
        self.assertRedirects(response, reverse('subject_detail', args=[self.edit_class.subject.code]))


class DataProcessorLoungeTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='user', password='pass')
        self.client.login(username='user', password='pass')
        
        # Crear una materia de prueba
        self.subject = Subject.objects.create(name='Materia de Prueba', code='123')
        
        # Crear una clase de prueba asociada a la materia de prueba
        self.edit_class = Class.objects.create(id='001', subject=self.subject)
        
    def test_data_processor_lounge_post_success_presencial(self):
        # Simular una solicitud POST exitosa al procesar datos para actualizar la clase (modalidad presencial)
        data = {
            'code_materia': '123',
            'code_clase': '001',
            'datetime1': '2024-04-25T08:00:00',
            'datetime2': '2024-04-25T10:00:00',
            'salon': '101D'
        }
        response = self.client.post(reverse('data_processor_lounge'), json.dumps(data), content_type='application/json')
        
        # Verificar que la respuesta sea exitosa
        self.assertEqual(response.status_code, 200)
        
        # Verificar que los datos se procesaron correctamente
        self.assertJSONEqual(response.content, {'mensaje': 'Datos procesados correctamente'})
        
        # Verificar que la modalidad de la clase se haya actualizado correctamente a presencial
        updated_class = Class.objects.get(id='001')
        self.assertEqual(updated_class.modality, 'PRESENCIAL')
        
    def test_data_processor_lounge_post_success_virtual(self):
        # Simular una solicitud POST exitosa al procesar datos para actualizar la clase (modalidad virtual)
        data = {
            'code_materia': '123',
            'code_clase': '001',
            'datetime1': '2024-04-25T08:00:00',
            'datetime2': '2024-04-25T10:00:00'
        }
        response = self.client.post(reverse('data_processor_lounge'), json.dumps(data), content_type='application/json')
        
        # Verificar que la respuesta sea exitosa
        self.assertEqual(response.status_code, 200)
        
        # Verificar que los datos se procesaron correctamente
        self.assertJSONEqual(response.content, {'mensaje': 'Datos procesados correctamente'})
        
        # Verificar que la modalidad de la clase se haya actualizado correctamente a virtual
        updated_class = Class.objects.get(id='001')
        self.assertEqual(updated_class.modality, 'VIRTUAL')

    def test_data_processor_lounge_post_invalid_modality(self):
        # Simular una solicitud POST con una modalidad inválida
        data = {
            'code_materia': '123',
            'code_clase': '001',
            'datetime1': '2024-04-25T08:00:00',
            'datetime2': '2024-04-25T10:00:00',
            'salon': '101D'
        }
        response = self.client.post(reverse('data_processor_lounge'), json.dumps(data), content_type='application/json')
        
        # Verificar que la solicitud devuelve un error
        self.assertEqual(response.status_code, 400)