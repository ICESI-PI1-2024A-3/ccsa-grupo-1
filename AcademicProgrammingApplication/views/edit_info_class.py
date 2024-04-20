from django.shortcuts import redirect, render
from AcademicProgrammingApplication.models import Class, Student
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from django.contrib import messages
from django.conf import settings
from django.core.mail import EmailMessage, send_mail
from datetime import datetime, timedelta
from django.shortcuts import get_object_or_404
import pytz
from celery import shared_task
from django.core.exceptions import ValidationError


def edit_info_class(request, class_id):
    """
    Renders a page for editing class information.

    Parameters:
        request (HttpRequest): The HTTP request object.
        class_id (int): The ID of the class to be edited.

    Returns:
        HttpResponse: Rendered HTML page for editing class information.
    """
    # Retrieve the authenticated user
    user = request.user
    # Get the class
    edit_class = Class.objects.filter(id=class_id).first()
    # Save changes within the class
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'save':
            edit_class.save()
            
            # Check if email should be sent
            if edit_class.send_email:
                # Call the function to send email
                send_email(request)
            
            return redirect('subject_detail', subject_id=edit_class.subject.code)
        elif action == 'cancel':
            return redirect('subject_detail', subject_id=edit_class.subject.code)
    # Render the edit-info-class page with necessary context data
    return render(request, 'edit-info-class.html', {
        'user_name': user.username,
        'title': 'Gestión de clases',
        'class': edit_class,
    })

processed_message = None
data_class_email = []

@csrf_exempt
def data_processor_lounge(request):
    global processed_message
    if request.method == 'POST':
        try:
            # Access JSON data sent from the frontend
            data_json = json.loads(request.body)
            
            # Process the data as needed
            code_materia = data_json['code_materia']
            code_clase = data_json['code_clase']
            datetime1 = data_json['datetime1']
            datetime2 = data_json['datetime2']
            if len(data_json) == 5:
                salon = data_json['salon']
            
            # Obtener la instancia de la clase que se actualizará
            clase = get_object_or_404(Class, id=code_clase)

            # Obtener la zona horaria de Colombia
            tz = pytz.timezone('America/Bogota')

            fecha_inicio = tz.localize(datetime.fromisoformat(datetime1))
            fecha_fin = tz.localize(datetime.fromisoformat(datetime2))
            
            # into to email
            data_class_email.append(code_materia)
            data_class_email.append(code_clase)
            data_class_email.append(datetime1)
            data_class_email.append(datetime2)
            if len(data_json) == 5:
                data_class_email.append(salon)

            print(data_class_email)
            print("entree a")
            # Actualizar las fechas de inicio y fin de la clase
            try:
                clase.start_date = fecha_inicio
                clase.ending_date = fecha_fin
                
                # Modificar el atributo send_email según sea necesario
                if clase.send_email:  # Si send_email es True
                    clase.send_email = False  # No se enviará correo electrónico después de actualizar
                else:
                    clase.send_email = True  # Se enviará correo electrónico después de actualizar
                    
                clase.save()
            except ValidationError as e:
                return JsonResponse({'mensaje': 'Error al actualizar la clase: {}'.format(str(e))}, status=500)
            
            # Return a JSON response indicating success
            processed_message = data_json
            return JsonResponse({'mensaje': 'Datos procesados correctamente'})
        except Exception as e:
            # If any error occurs during data processing,
            # return an error message
            return JsonResponse({'error': str(e)}, status=500)
    else:
        # Return a JSON response indicating that the method is not allowed
        return JsonResponse({'error': 'Método no permitido'}, status=405)




    
def send_email(request):
    global processed_message, data_class_email
    if processed_message is not None:
        if len(processed_message) == 5:
            email_mensaje = "la nueva fecha de la clase: inicio " + data_class_email[2] + " y finaliza " + data_class_email[3] + " y será en salón: " + data_class_email[4]
        elif len(processed_message) == 4:
            email_mensaje = "la nueva fecha de la clase: inicio " + data_class_email[2] + " y finaliza " + data_class_email[3]

        # Get the subject_id
        subject_id = data_class_email[0]

        # Query all students related to the subject
        students = Student.objects.filter(subject__code=subject_id)

        # Construct the email content
        subject = 'Subject of the Email'
        message = ""
        for student in students:
            message += f"Para {student.name},\n\n"
            message += f"Nuevo horario de clase: {email_mensaje}.\n\n"
            message += "Regards,\nYour Name\n\n"

        # Set the new date to send the email
        fecha_inicio = datetime.fromisoformat(data_class_email[2])
        enviar_correo_12h_antes_de_inicio_clase.delay(subject, message, students, fecha_inicio)
    else:
        email_mensaje = "Mensaje de correo no disponible"
    
    

    




# tasks to send email
@shared_task
def enviar_correo_programado(subject, message, student_email):
    email = EmailMessage(
        subject,
        message,
        settings.EMAIL_HOST_USER,  # Dirección de correo electrónico del remitente
        [student_email]  # Lista de destinatarios, en este caso, el correo electrónico del estudiante
    )
    email.send()

@shared_task
def enviar_correo_12h_antes_de_inicio_clase(subject, message, student_email, start_time):
    start_time_minus_12h = start_time - timedelta(hours=12)
    now = datetime.now()
    if now < start_time_minus_12h:
        enviar_correo_programado.apply_async((subject, message, student_email), eta=start_time_minus_12h)




@csrf_exempt
def edit_class_date_information(request):
    
    if request.method == 'POST':
        try:
            # Access JSON data sent from the frontend
            data_json = json.loads(request.body)
            
            # Process the data as needed
            code_materia = data_json['code_materia']
            code_clase = data_json['code_clase']
            datetime1 = data_json['datetime1']
            
            
            # Obtener la instancia de la clase que se actualizará
            clase = get_object_or_404(Class, id=code_clase)

            # Obtener la zona horaria de Colombia
            tz = pytz.timezone('America/Bogota')

            fecha_inicio = tz.localize(datetime.fromisoformat(datetime1))
            
    
            print('actualice fecha de clase')
            
            # Actualizar las fechas de inicio y fin de la clase
            try:
                clase.start_date = fecha_inicio
                clase.send_email = True
                clase.save()
            except ValidationError as e:
                return JsonResponse({'mensaje': 'Error al actualizar la clase: {}'.format(str(e))}, status=500)
            
            # Return a JSON response indicating success
            
            return JsonResponse({'mensaje': 'Datos actualizados cotrectamente'})
        except Exception as e:
            # If any error occurs during data processing,
            # return an error message
            return JsonResponse({'error': str(e)}, status=500)
    else:
        # Return a JSON response indicating that the method is not allowed
        return JsonResponse({'error': 'Método no permitido'}, status=405)
    