from django.shortcuts import render
import pandas as pd
from datetime import datetime
from AcademicProgrammingApplication.models import Archivo


def planning_proposal(request):
    archivos = Archivo.objects.all()
    archivo_seleccionado = None

    if request.method == 'POST' and request.FILES.get('archivo'):
        archivo_subido = request.FILES['archivo']
        nuevo_nombre = f"Programacion_{datetime.now().strftime('%d-%m-%Y_%H%M%S')}.xlsx"
        archivo_subido.name = nuevo_nombre  

        try:
            ultimo_archivo = Archivo.objects.latest('id')
            ultimo_archivo.nombre_archivo = nuevo_nombre
            ultimo_archivo.path = archivo_subido  
            ultimo_archivo.save()
        except Archivo.DoesNotExist:
            Archivo.objects.create(nombre_archivo=nuevo_nombre, path=archivo_subido)

        # Procesar el archivo recién subido para mostrar detalles en la tabla de abajo
        df = pd.read_excel(archivo_subido)
        
        # Filtrar las filas que contienen información en la columna 'Comentario'
        df = df[df['Comentario'].notna()]
        
        # Seleccionar solo las columnas especificadas
        df = df[['Nombre_Profesor', 'Fecha_Inicio', 'Comentario', 'Nombre_Materia']]
        
        # Asignar el DataFrame filtrado a archivo_seleccionado
        archivo_seleccionado = df.to_dict(orient='records')
        print(archivo_seleccionado)
    
    return render(request, 'academic-programming-proposal.html', {
        'title': 'Propuesta Programacion Academica',
        'archivos': archivos,
        'archivo_seleccionado': archivo_seleccionado,
    })