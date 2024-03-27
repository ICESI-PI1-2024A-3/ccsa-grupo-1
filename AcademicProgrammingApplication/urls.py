from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('accounts/sing-up', views.sing_up, name='sing-up'),
    # path('base', views.base_screen, name='base'),
    path('home', login_required(views.academic_management), name='home'),
    path('logout', login_required(views.logout), name='logout'),
    path('assign/', login_required(views.assign_teacher), name='assign_teacher'),
    path('search/', login_required(views.search_teacher), name='search_teacher'),
]