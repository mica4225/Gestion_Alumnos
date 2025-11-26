from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Alumno
from .forms import AlumnoForm
from django.http import HttpResponse
from django.core.mail import EmailMessage
from reportlab.pdfgen import canvas
from io import BytesIO

@login_required
def dashboard(request):
    alumnos = Alumno.objects.filter(usuario=request.user)
    return render(request, 'alumnos/dashboard.html', {'alumnos': alumnos})

@login_required
def alumno_create(request):
    if request.method == 'POST':
        form = AlumnoForm(request.POST)
        if form.is_valid():
            al = form.save(commit=False)
            al.usuario = request.user
            al.save()
            return redirect('alumnos:dashboard')
    else:
        form = AlumnoForm()
    return render(request, 'alumnos/alumno_form.html', {'form': form})

@login_required
def alumno_detail(request, pk):
    al = get_object_or_404(Alumno, pk=pk, usuario=request.user)
    return render(request, 'alumnos/alumno_detail.html', {'alumno': al})

# Generar PDF y enviar por email
@login_required
def enviar_pdf_por_correo(request, pk):
    al = get_object_or_404(Alumno, pk=pk, usuario=request.user)

    # 1) Generar PDF en memoria
    buffer = BytesIO()
    p = canvas.Canvas(buffer)
    p.setFont("Helvetica", 14)
    p.drawString(100, 800, f"Ficha del alumno: {al.nombre}")
    p.drawString(100, 770, f"Correo: {al.correo}")
    p.drawString(100, 740, f"Curso: {al.curso}")
    p.drawString(100, 710, f"Creado: {al.creado.strftime('%Y-%m-%d %H:%M')}")
    p.showPage()
    p.save()
    buffer.seek(0)

    # 2) Enviar email con adjunto (al docente o al mismo usuario)
    subject = f"Ficha de {al.nombre}"
    body = f"Adjunto se envía la ficha del alumno {al.nombre}."
    to_email = request.user.email  # o poné el email del docente
    email = EmailMessage(subject, body, to=[to_email])
    email.attach(f"{al.nombre}.pdf", buffer.read(), 'application/pdf')
    try:
        email.send(fail_silently=False)
    except Exception as e:
        return HttpResponse(f"Error enviando email: {e}", status=500)

    return redirect('alumnos:dashboard')
def alumno_create(request):
    if request.method == "POST":
        form = AlumnoForm(request.POST)
        if form.is_valid():
            alumno = form.save(commit=False)
            alumno.usuario = request.user     
            alumno.save()

            return redirect('alumnos:dashboard')
    else:
        form = AlumnoForm()
    
    return render(request, 'alumnos/alumno_form.html', {'form': form})