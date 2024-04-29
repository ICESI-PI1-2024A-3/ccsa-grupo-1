from django.urls import path
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from . import views
from .views.viatic_views import save_viatic

urlpatterns = [
    # Lines used to see how the base HTML looks like
    path('base', views.base_screen, name='base'),
    # Application views
    path('', views.login, name='login'),
    path('accounts/sign_up/', login_required(views.sign_up), name='sign_up'),
    path('home', login_required(views.academic_management), name='home'),
    path('logout', login_required(views.logout), name='logout'),
    path('assign/<str:class_id>/', login_required(views.assign_teacher), name='assign_teacher'),
    path('search/', login_required(views.search_teacher), name='search_teacher'),
    path('subject/<str:subject_id>/', login_required(views.subject_detail), name='subject_detail'),
    path('accounts/password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('accounts/reset_password_sent', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('accounts/reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('accounts/reset_password_confirm/', auth_views.PasswordResetCompleteView.as_view(),
         name='password_reset_complete'),
    path('home/delete_academic_program/<int:program_id>/', login_required(views.delete_academic_program),
         name='delete_academic_program'),
    path('home/academic_program_edition/<int:program_id>/', login_required(views.academic_program_edition),
         name='academic_program_edition'),
    path('home/edit_academic_program/<int:program_id>/', login_required(views.edit_academic_program),
         name='edit_academic_program'),
    path('edit_class/<str:class_id>/', login_required(views.edit_info_class), name='edit_info_class'),
    path('teacher_management/', login_required(views.teacher_management), name='teacher_management'),
    path('teacher/<str:teacher_id>/', login_required(views.teacher_detail), name='teacher_detail'),
    path('save_viatic/', login_required(save_viatic), name='save_viatic'),
    path('planning_proposal/', views.planning_proposal, name='planning_proposal'),
    path('role_management/', views.role_management, name='role_management'),
]
