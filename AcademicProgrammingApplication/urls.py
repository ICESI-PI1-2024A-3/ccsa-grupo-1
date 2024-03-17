from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    path('accounts/login/', views.login, name='login'),
    path('sing-up', views.sing_up, name='sing-up'),
    # path('base', views.base_screen, name='base'),
    path('home', login_required(views.academic_management), name='academic-management'),
    path('logout', login_required(views.logout), name='logout'),
]
