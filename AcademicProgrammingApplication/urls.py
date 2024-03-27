from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    # Lines used to see how the base HTML looks like
    path('base', views.base_screen, name='base'),
    # Application views
    path('', views.login, name='login'),
    path('accounts/sign-up', views.sign_up, name='sign-up'),
    path('home', login_required(views.academic_management), name='home'),
    path('logout', login_required(views.logout), name='logout'),
    path('assign/', login_required(views.assign_teacher), name='assign_teacher'),
    path('search/', login_required(views.search_teacher), name='search_teacher'),
    path('classes/<int:teacher_id>', login_required(views.get_classes), name='get_classes'),
    path('subject/<int:subject_id>/', views.subject_detail, name='subject_detail'),
    path('accounts/forgot-password', views.forgot_password, name='forgot-password'),
]
