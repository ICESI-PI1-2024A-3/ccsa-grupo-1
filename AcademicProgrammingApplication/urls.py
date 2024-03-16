from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('sing-up', views.sing_up, name='sing-up'),
    path('base', views.base_screen, name='base'),
    path('home', views.academic_management, name='academic-management'),
    path('logout', views.logout, name='logout'),
]
