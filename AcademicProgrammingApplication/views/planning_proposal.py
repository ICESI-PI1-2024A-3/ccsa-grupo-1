from django.shortcuts import render, redirect
from datetime import datetime
from AcademicProgrammingApplication.models import Archivo
from AcademicProgrammingApplication.forms import UploadFileForm

def planning_proposal(request):
    if request.method == 'POST' and request.FILES.get('archivo'):
        archivo_subido = request.FILES['archivo']
        nuevo_nombre = f"Programacion_{datetime.now().strftime('%d-%m-%Y_%H%M%S')}.xlsx"
        archivo_subido.name = nuevo_nombre  # Cambiar el nombre del archivo

        try:
            ultimo_archivo = Archivo.objects.latest('id')
            ultimo_archivo.nombre_archivo = nuevo_nombre
            ultimo_archivo.path = archivo_subido  # Asumiendo que 'path' es un FileField o similar
            ultimo_archivo.save()
        except Archivo.DoesNotExist:
            Archivo.objects.create(nombre_archivo=nuevo_nombre, path=archivo_subido)

        return redirect('planning_proposal')  # Reemplaza con el nombre real de tu vista

    archivos = Archivo.objects.all()
    return render(request, 'academic-programming-proposal.html', {
        'title': 'Propuesta Programacion Academica',
        'archivos': archivos,
    })