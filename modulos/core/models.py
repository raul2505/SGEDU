from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    dni = models.CharField(max_length=8, unique=True)
    telefono = models.CharField(max_length=15, unique=True)
    direccion = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return f"{self.username}"

class PerfilDocente(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    especialidad = models.CharField(max_length=20)

    def __str__(self):
        return f"Docente: {self.usuario.get_full_name()}"

class PerfilEstudiante(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    grado = models.CharField(max_length=10)
    seccion = models.CharField(max_length=5)
    fecha_nacimiento = models.DateField()

    def __str__(self):
        return f"Estudiante: {self.usuario.get_full_name()}"

class PerfilPadre(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    hijos = models.ManyToManyField(PerfilEstudiante, related_name='padres')

    def __str__(self):
        return f"Padre/Tutor: {self.usuario.get_full_name()}"

class PerfilMedico(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    registro_profesional = models.CharField(max_length=50)

    def __str__(self):
        return f"Médico: {self.usuario.get_full_name()}"

class PerfilAdministrativo(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    cargo = models.CharField(max_length=100)

    def __str__(self):
        return f"Administrativo: {self.usuario.get_full_name()}"
