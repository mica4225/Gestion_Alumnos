from django.urls import path
from django.shortcuts import redirect
from . import views

app_name = 'alumnos'

urlpatterns = [
    path('', lambda request: redirect('alumnos:dashboard')),  # 👈 nueva
    path('dashboard/', views.dashboard, name='dashboard'),
    path('crear/', views.alumno_create, name='alumno_create'),
    path('alumno/<int:pk>/', views.alumno_detail, name='alumno_detail'),
    path('alumno/<int:pk>/enviar_pdf/', views.enviar_pdf_por_correo, name='enviar_pdf_por_correo'),
]
