from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    # Lines used to see how the base HTML looks like
    path('edit', views.edit_screen, name='edit'),


#This will change     
#   path('editSubject/<int:nrc>',SubjectFormView.edit, name='editSubject'),
]
