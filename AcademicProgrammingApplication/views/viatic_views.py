from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from AcademicProgrammingApplication.models import Teacher, Viatic


class ViaticView:
    @staticmethod
    @csrf_exempt
    def save_viatic(request):
        """
        Saves a viatic request.

        Parameters:
            request (HttpRequest): The HTTP request object.

        Returns:
            JsonResponse: JSON response indicating success or failure.
        """
        if request.method == 'POST':
            data = json.loads(request.body)
            teacher = Teacher.objects.get(id=data['id_teacher'])
            viatico = Viatic.objects.create(
                transport=data['tiquetes'] == 'Si',
                accommodation=data['hotel'] == 'Si',
                viatic=data['viatico'] == 'Si',
                viatic_status='ENVIADA',
                id_teacher=teacher
            )

            ViaticView.send_email_after_update(teacher, viatico)

            return JsonResponse({'message': 'Viatico creado exitosamente'}, status=201)
        else:
            return JsonResponse({'error': 'Invalid method'}, status=400)

    @staticmethod
    def send_email_after_update(teacher, viatico):
        """
        Sends an email notification after updating viatic information.

        Parameters:
            teacher (Teacher): The teacher associated with the viatic request.
            viatico (Viatic): The viatic request object.

        Returns:
            None
        """
        subject = 'Solicitud de viático'
        message = f"Se ha solicitado un viático con el identificador '{viatico.id}' para el profesor {teacher.name}. Esperamos pronta revisión y procesamiento de esta solicitud.\n\nResumen:\n- Tiquetes: {'Sí' if viatico.transport else 'No'}\n- Hotel: {'Sí' if viatico.accommodation else 'No'}\n- Viáticos: {'Sí' if viatico.viatic else 'No'}"
        from_email = 'programacion_academica@example.com'
        to_emails = ['oficinaplaneacion573@gmail.com']
        send_mail(subject, message, from_email, to_emails)
