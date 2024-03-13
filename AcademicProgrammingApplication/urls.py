from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    # Lines used to see how the base HTML looks like
    path('base', views.base_screen, name='base'),
    path('spam', views.spam, name='spam'),


    # The next line is used to process the data sent from the frontend
    path('dataProcessor_lounge/', views.data_processor_lounge , name='data_processor_lounge')
]
