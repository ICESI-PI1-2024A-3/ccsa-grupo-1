from django.shortcuts import render
from AcademicProgrammingApplication.models import Teacher, Contract, Class

def teacher_detail(request, teacher_id):
    # Retrieve the authenticated user
    user = request.user
    # Get the teacher based on the provided teacher_id
    teacher = Teacher.objects.get(id=teacher_id)
    # Render the teacher management page with necessary context data
    return render(request, 'teacher-detail.html', {
        'title': 'Gestión de Profesores',
        'user_name': user.username,
        'teacher': teacher,
        'classes': get_classes(teacher),
    })

# Get the classes associated with a given teacher ID
def get_classes(teacher_id):
    """
    Get the classes associated with a given teacher ID.

    Returns:
        list: List of dictionaries containing class information.
    """
    # Get the classes associated with a given teacher
    classes = Class.objects.filter(teacher_id=teacher_id).all()
    # Initialize the array of out
    out = []
    # Get the most important information of the classes
    for session in classes:
        out.append({
            'title': session.subject.name,
            'start': session.start_date.strftime('%Y-%m-%dT%H:%M:%S'),
            'end': session.ending_date.strftime('%Y-%m-%dT%H:%M:%S')
        })
    return out