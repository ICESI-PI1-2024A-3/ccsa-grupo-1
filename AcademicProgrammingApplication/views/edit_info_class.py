from django.shortcuts import redirect, render
from AcademicProgrammingApplication.models import Class
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from django.contrib import messages
from django.conf import settings
from django.core.mail import EmailMessage


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
@csrf_exempt
def data_processor_lounge(request):
    global processed_message
    if request.method == 'POST':
        try:
            # Access JSON data sent from the frontend
            data_json = json.loads(request.body)
            
            # Process the data as needed
            
            # Return a JSON response indicating success
            print(data_json)
            print(type(data_json))
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
    if processed_message is not None:
        if len(processed_message) == 3:

            email_mensseje = "la nueva fecha de la clase: inicio " + str(processed_message.get('datetime1')) + " y final " + str(processed_message.get('datetime2')) + " y será en salón: " + str(processed_message.get('salon'))
        elif len(processed_message) == 2:
            email_mensseje = "la nueva fecha de la clase virrtual sera: inicio " + str(processed_message.get('datetime1')) + " y final " + str(processed_message.get('datetime2'))
    else:
        email_mensseje = "Mensaje de correo no disponible"
    print(email_mensseje)

    if request.method == 'POST':
        # Get information from the POST form
        subject_id = request.POST.get('code')  
        
        # Query all students related to the subject
        #students = Student.objects.filter(subject__code=subject_id)
        
        # Build the email content
        subject = 'Subject of the Email'
        print('hasta aqui llega')
        # Send the email to each student
        #students = Student.objects.filter(subject__code=subject_id)

        # Build the email content
        subject = 'Subject of the Email'
            
        # Construct the message content
        message = f"Para {' carlos tafurt'},\n\n"
        message += f"Nuevo horario de clase {email_mensseje}.\n\n"
        message += "Regards,\nYour Name"

        # Send the email
        email = EmailMessage(
            subject,
            message,
            settings.EMAIL_HOST_USER,  # Sender's email address
            ['carlost1504@gmail.com'],
            ##[student.email]  # List of recipients, in this case, the student's email
        )
        print('mensaje_enviado')
        email.fail_silently = False
        email.send()

        messages.success(request, 'Email sent successfully')
        # You can return an appropriate HTTP response if desired
        return render(request, 'edit-info-class.html')

