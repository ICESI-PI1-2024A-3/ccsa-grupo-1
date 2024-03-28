from django.shortcuts import render
from AcademicProgrammingApplication.models import Student
from .forms import UserForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib import messages

# Create your views here.
def login(request):
    # print(request.POST)
    return render(request, 'login.html', {
        'form': UserForm()
    })


# The next lines are only used to see how the base HTML looks like
def base_screen(request):
    return render(request, 'layouts/base-app-pages.html', {
        'user_name': "Carlos",
        'title': 'Main page',
    })

def spam(request):
    return render(request, 'SpamDate.html', {
        'user_name': "Carlos",
        'title': 'Main page',
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
    if request.method == 'POST':
        # Get information from the POST form
        subject_id = request.POST.get('code')  
        
        # Query all students related to the subject
        students = Student.objects.filter(subject__code=subject_id)
        
        # Build the email content
        subject = 'Subject of the Email'

        # Send the email to each student
        for student in students:

            template= render_to_string('email_templete.html',
            {
                'student': student.name,
                'email': student.email,
                'message': 'new hours the class is ' + str(processed_message),

            })

            email = EmailMessage(
                subject,
                template,
                settings.EMAIL_HOST_USER,  # Sender's email address
                [student.email]  # List of recipients, in this case, the student's email
            )
            email.fail_silently = False
            email.send()

        messages.success(request, 'Email sent successfully')
        # You can return an appropriate HTTP response if desired
        return render(request, 'SpamDate.html')