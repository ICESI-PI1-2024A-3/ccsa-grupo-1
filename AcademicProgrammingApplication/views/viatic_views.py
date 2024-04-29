import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from AcademicProgrammingApplication.models import Viatic, Teacher


@csrf_exempt
def save_viatic(request):
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
        return JsonResponse({'message': 'Viatico creado exitosamente'}, status=201)
    else:
        return JsonResponse({'error': 'Invalid method'}, status=400)
