from django.shortcuts import redirect, render
from AcademicProgrammingApplication.models import Class, Student
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from django.contrib import messages
from django.conf import settings
from django.core.mail import EmailMessage
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
            email_content = generate_class_email_content(edit_class)
            mensaje = f"Estimado {edit_class.teacher},\n\n"
            mensaje += f"Aquí están los detalles para la próxima clase:\n\n{email_content}\n\n"
            mensaje += "Saludos,\nTu Nombre"

            # Check if email should be sent
            if edit_class.send_email:
                data_json = {
                    'code_materia': edit_class.subject.code,
                    'code_clase': edit_class.id,
                    'datetime1': edit_class.start_date.isoformat(),
                    'datetime2': edit_class.ending_date.isoformat(),
                    'salon': edit_class.classroom,
                    'modality': edit_class.modality
                }
                process_data(data_json)

            # Envía el correo electrónico
            try:
                email = EmailMessage(
                    'Class Information',
                    mensaje,
                    settings.EMAIL_HOST_USER,  # Dirección de correo electrónico del remitente
                    [edit_class.teacher.email],
                    # Lista de destinatarios, en este caso, el correo electrónico del profesor
                )
                email.send()
                messages.success(request, 'Email sent successfully')
            except Exception as e:
                messages.error(request, f'Failed to send email: {str(e)}')

            return redirect('subject_detail', subject_id=edit_class.subject.code)
        elif action == 'cancel':
            return redirect('subject_detail', subject_id=edit_class.subject.code)
    # Render the edit-info-class page with necessary context data
    return render(request, 'edit-info-class.html', {
        'user_name': user.username,
        'user_role': user.role,
        'title': 'Gestión de clases',
        'change_role_permission': user.has_perm('AcademicProgrammingApplication.change_role'),
        'class': edit_class,
    })


@csrf_exempt
def data_processor_lounge(request):
    """
    Processes data related to classroom.

    Parameters:
        request (HttpRequest): The HTTP request object.

    Returns:
        JsonResponse: JSON response indicating success or failure of data processing.
    """
    if request.method == 'POST':
        try:
            data_json = json.loads(request.body)
            process_data(data_json)
            update_class_schedule(data_json)
            send_email_after_update(data_json)

            return JsonResponse({'mensaje': 'Datos procesados correctamente'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)


def process_data(data_json):
    """
    Process the JSON data related to a class.

    Parameters:
        data_json (dict): JSON data containing class information.

    Returns:
        list: Processed data.
    """
    code_materia = data_json['code_materia']
    code_clase = data_json['code_clase']
    datetime1 = data_json['datetime1']
    datetime2 = data_json['datetime2']
    salon = data_json.get('salon', None)
    modality = data_json.get('modality')

    processed_data = [code_materia, code_clase, datetime1, datetime2, salon, modality]
    return processed_data


def update_class_schedule(data_json):
    """
    Updates the schedule of a class based on provided data.

    Parameters:
        data_json (dict): JSON data containing class information.
    """
    code_clase = data_json['code_clase']
    clase = get_object_or_404(Class, id=code_clase)

    new_modality = 'PRESENCIAL' if len(data_json) == 5 else 'VIRTUAL'
    if new_modality not in [choice[0] for choice in Class.MODALITY_CHOICES]:
        raise ValueError('Modalidad no válida')
    clase.modality = new_modality

    tz = pytz.timezone('America/Bogota')
    start_date = tz.localize(datetime.fromisoformat(data_json['datetime1']))
    end_date = tz.localize(datetime.fromisoformat(data_json['datetime2']))

    clase.start_date = start_date
    clase.ending_date = end_date

    clase.send_email = False

    if len(data_json) == 6:
        clase.modality = 'PRESENCIAL'
        clase.link = None
        clase.classroom = 'c202'
    elif len(data_json) == 5:
        clase.modality = 'VIRTUAL'
        clase.classroom = None
        clase.link = 'https://zoom.us/j/1234567890'

    clase.save()


def send_email_after_update(data_json):
    """
    Sends email notification after updating class information.

    Parameters:
        data_json (dict): JSON data containing class information.
    """
    if data_json is not None:
        if len(data_json) == 6:
            email_mensaje = f"la nueva fecha de la clase: inicio {data_json['datetime1']} y finaliza {data_json['datetime2']} y será en salón: {data_json['salon']}"
        elif len(data_json) == 5:
            email_mensaje = f"la nueva fecha de la clase: inicio {data_json['datetime1']} y finaliza {data_json['datetime2']}"
        else:
            email_mensaje = "Mensaje de correo no disponible"

        subject_id = data_json['code_materia']
        students = Student.objects.filter(subject__code=subject_id)
        subject = 'Subject of the Email'
        message = ""
        for student in students:
            message += f"Para {student.name},\n\n"
            message += f"Nuevo horario de clase: {email_mensaje}.\n\n"
            message += "Regards,\nYour Name\n\n"
        fecha_inicio = datetime.fromisoformat(data_json['datetime1'])
        enviar_correo_12h_antes_de_inicio_clase.delay(subject, message, students, fecha_inicio)
    else:
        email_mensaje = "Mensaje de correo no disponible"


@shared_task
def send_scheduled_mail(subject, message, student_email):
    """
    Sends scheduled email.

    Parameters:
        subject (str): Email subject.
        message (str): Email message.
        student_email (str): Email address of the student.
    """
    email = EmailMessage(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [student_email]
    )
    email.send()


@shared_task
def enviar_correo_12h_antes_de_inicio_clase(subject, message, student_email, start_time):
    """
    Sends email 12 hours before class starts.

    Parameters:
        subject (str): Email subject.
        message (str): Email message.
        student_email (str): Email address of the student.
        start_time (datetime): Start time of the class.
    """
    start_time_minus_12h = start_time - timedelta(hours=12)
    now = datetime.now()
    if now < start_time_minus_12h:
        send_scheduled_mail.apply_async((subject, message, student_email), eta=start_time_minus_12h)


@csrf_exempt
def edit_class_date_information(request):
    """
    Edits class date information.

    Parameters:
        request (HttpRequest): The HTTP request object.

    Returns:
        JsonResponse: JSON response indicating success or failure of data editing.
    """
    if request.method == 'POST':
        try:
            data_json = json.loads(request.body)
            code_clase = data_json['code_clase']
            datetime1 = data_json['datetime1']
            clase = get_object_or_404(Class, id=code_clase)
            fecha_inicio = datetime.fromisoformat(datetime1)
            fecha_inicio = fecha_inicio.replace(tzinfo=pytz.UTC)

            try:
                clase.start_date = fecha_inicio
                clase.send_email = True
                clase.save()

            except ValidationError as e:
                return JsonResponse({'mensaje': 'Error al actualizar la clase: {}'.format(str(e))}, status=500)

            return JsonResponse({'mensaje': 'Datos actualizados correctamente'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)


@csrf_exempt
def update_end_date_class(request):
    """
    Updates the end date of a class.

    Parameters:
        request (HttpRequest): The HTTP request object.

    Returns:
        JsonResponse: JSON response indicating success or failure of data updating.
    """
    if request.method == 'POST':
        try:
            data_json = json.loads(request.body)
            code_clase = data_json['code_clase']
            datetime1 = data_json['datetime1']
            clase = get_object_or_404(Class, id=code_clase)
            fecha_inicio = datetime.fromisoformat(datetime1)
            fecha_inicio = fecha_inicio.replace(tzinfo=pytz.UTC)

            try:
                clase.ending_date = fecha_inicio
                clase.send_email = True
                clase.save()
            except ValidationError as e:
                return JsonResponse({'mensaje': 'Error al actualizar la clase: {}'.format(str(e))}, status=500)

            return JsonResponse({'mensaje': 'Datos actualizados correctamente'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)


def generate_class_email_content(class_instance):
    """
    Generates email content with class information.

    Parameters:
        class_instance (Class): Class instance.

    Returns:
        str: Email content.
    """
    email_content = ""
    email_content += f"Número de Sesión: {class_instance.id}\n"
    email_content += f"Fecha de Inicio: {class_instance.start_date}\n"
    email_content += f"Fecha de Finalización: {class_instance.ending_date}\n"
    email_content += f"Modalidad: {class_instance.modality}\n"
    email_content += f"Aula: {class_instance.classroom}\n"
    email_content += f"Enlace de Plataforma Virtual: {class_instance.link}\n"
    email_content += f"Enviar Email: {class_instance.send_email}\n"
    email_content += f"Asignatura Asociada: {class_instance.subject}\n"
    email_content += f"Profesor Asociado: {class_instance.teacher}\n"

    return email_content
