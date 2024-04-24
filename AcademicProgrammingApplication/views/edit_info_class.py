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
                data_processor_lounge(request)
            
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
    if request.method == 'POST':
        try:
            data_json = json.loads(request.body)
            print(data_json)
            print(len(data_json))
            print(type(data_json))
            process_data(data_json)
            update_class_schedule(data_json)
            send_email_after_update(data_json)

            return JsonResponse({'mensaje': 'Datos procesados correctamente'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)

def process_data(data_json):
    global data_class_email
    code_materia = data_json['code_materia']
    code_clase = data_json['code_clase']
    datetime1 = data_json['datetime1']
    datetime2 = data_json['datetime2']
    salon = data_json.get('salon', None)
    modality = data_json.get('modality')

    data_class_email = [code_materia, code_clase, datetime1, datetime2, salon, modality]
    print(data_class_email)

def update_class_schedule(data_json):
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
        print('clase presencial')
    elif len(data_json) == 5:
        clase.modality = 'VIRTUAL'
        clase.classroom= None
        clase.link = 'https://zoom.us/j/1234567890'
        print('clase virtual')

    print(clase.modality)
    

    clase.save()

def send_email_after_update(data_json):
    global data_class_email
    if data_json is not None:
        if len(data_json) == 6:
            email_mensaje = f"la nueva fecha de la clase: inicio {data_class_email[2]} y finaliza {data_class_email[3]} y será en salón: {data_class_email[4]}"
        elif len(data_json) == 5:
            email_mensaje = f"la nueva fecha de la clase: inicio {data_class_email[2]} y finaliza {data_class_email[3]}"
        else:
            email_mensaje = "Mensaje de correo no disponible"

        subject_id = data_class_email[0]
        students = Student.objects.filter(subject__code=subject_id)
        subject = 'Subject of the Email'
        message = ""
        for student in students:
            message += f"Para {student.name},\n\n"
            message += f"Nuevo horario de clase: {email_mensaje}.\n\n"
            message += "Regards,\nYour Name\n\n"
        fecha_inicio = datetime.fromisoformat(data_class_email[2])
        send_mail_12h_before_start_class.delay(subject, message, students, fecha_inicio)
    else:
        email_mensaje = "Mensaje de correo no disponible"
    
    

    




# tasks to send email
@shared_task
def send_scheduled_mail(subject, message, student_email):
    email = EmailMessage(
        subject,
        message,
        settings.EMAIL_HOST_USER,  # Sender email address
        [student_email]  # Recipient list, in this case the student's email
    )
    email.send()

@shared_task #send_mail_12h_before_start_class
def send_mail_12h_before_start_class(subject, message, student_email, start_time):
    start_time_minus_12h = start_time - timedelta(hours=12)
    now = datetime.now()
    if now < start_time_minus_12h:
        
        send_scheduled_mail.apply_async((subject, message, student_email), eta=start_time_minus_12h)



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
            
            
            # Get the instance of the class to be updated
            clase = get_object_or_404(Class, id=code_clase)

            # Get Colombia time zone
            tz = pytz.timezone('America/Bogota')

            fecha_inicio = tz.localize(datetime.fromisoformat(datetime1))
            
    
            print('actualice fecha de clase')
            
            # Update class start and end dates
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
    