from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('sing-up', views.sing_up, name='sing-up'),
    # Lines used to see how the base HTML looks like
    path('base', views.base_screen, name='base'),
    path('home', views.academic_management, name='academic-management')
]
