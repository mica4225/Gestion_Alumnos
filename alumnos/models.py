from django.db import models
from django.contrib.auth.models import User

class Alumno(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)  # owner
    nombre = models.CharField(max_length=200)
    dni = models.CharField(max_length=20)
    correo = models.EmailField()
    curso = models.CharField(max_length=100)
    creado = models.DateTimeField(auto_now_add=True)

    fecha_inscripcion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Alumno'
        verbose_name_plural = 'Alumnos'
        ordering = ['-fecha_inscripcion']

    def __str__(self):
        return self.nombre