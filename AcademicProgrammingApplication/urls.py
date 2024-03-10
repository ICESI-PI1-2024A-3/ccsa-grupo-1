from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    # Lines used to see how the base HTML looks like
    # path('base', views.base_screen, name='base'),
]
