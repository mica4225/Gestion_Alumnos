# usuarios/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from .forms import RegistroForm
from django.conf import settings

def register_view(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            # envío de correo de bienvenida
            subject = "Bienvenido a la plataforma"
            html = render_to_string('usuarios/bienvenida.html', {'user': user})
            email = EmailMessage(subject, html, settings.DEFAULT_FROM_EMAIL, ['maf.micaela@gmail.com'])
            email.content_subtype = 'html'
            try:
                email.send(fail_silently=False)
            except Exception as e:
                # loggear o manejar error
                print("Error enviando email:", e)
            login(request, user)
            return redirect('alumnos:dashboard')
    else:
        form = RegistroForm()
    return render(request, 'usuarios/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('alumnos:dashboard')
        else:
            return render(request, 'usuarios/login.html', {'error':'Credenciales inválidas'})
    return render(request, 'usuarios/login.html')

def logout_view(request):
    logout(request)
    return redirect('usuarios:login')
