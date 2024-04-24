from django.shortcuts import render
import pandas as pd
from datetime import datetime
from AcademicProgrammingApplication.models import File


def planning_proposal(request):
    files = File.objects.all()
    file_selected = None

    if request.method == 'POST' and request.FILES.get('file'):
        updated_file = request.FILES['file']
        new_name = f"Programacion_{datetime.now().strftime('%d-%m-%Y_%H%M%S')}.xlsx"
        updated_file.name = new_name  

        try:
            last_file = File.objects.latest('id')
            last_file.name_file = new_name
            last_file.path = updated_file
  
            last_file.save()
        except File.DoesNotExist:
            File.objects.create(name_file=new_name, path=updated_file
)
        df = pd.read_excel(updated_file)

        df = df[df['Comentario'].notna()]

        df = df[['Nombre_Profesor', 'Fecha_Inicio', 'Comentario', 'Nombre_Materia']]
        
        df['id'] = range(1, len(df) + 1)
        
        file_selected = df.to_dict(orient='records')
        print(file_selected)
    
    return render(request, 'academic-programming-proposal.html', {
        'title': 'Propuesta Programacion Academica',
        'files': files,
        'file_selected': file_selected,
    })