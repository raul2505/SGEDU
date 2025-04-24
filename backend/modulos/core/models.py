from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator

#USUARIO
class Usuario(AbstractUser):
    GENERO = [('M', 'Masculino'), ('F', 'Femenino')]
    
    foto_perfil = models.ImageField(
        upload_to='foto_perfil/',
        default='foto_perfil/default.png',
        blank=True
    )
    dni = models.CharField(
        max_length=8,
        unique=True,
        validators=[RegexValidator(r'^\d+$', 'Solo números permitidos.')]
    )
    fecha_nacimiento = models.DateField(null=True, blank=True)
    genero = models.CharField(max_length=1, choices=GENERO, blank=True)
    correo_institucional = models.EmailField(unique=True, blank=True)
    departamento = models.CharField(max_length=30, blank=True)
    distrito = models.CharField(max_length=30, blank=True)
    provincia = models.CharField(max_length=30, blank=True)
    telefono = models.CharField(
        max_length=15,
        unique=True,
        validators=[RegexValidator(r'^\+?\d{9,15}$', 'Formato: +[código][número]')]
    )
    direccion = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.username

    def nombre_completo(self):
        return f"{self.first_name} {self.last_name}".strip()

#PERFILES DE USUARIOS

class PerfilDocente(models.Model):
    GRADO_EDUCACION_CHOICES = [
        ('BACH', 'Bachiller'),
        ('LIC', 'Licenciado'),
        ('MG', 'Magíster'),
        ('DR', 'Doctor'),
        ('OTRO', 'Otro')
    ]
    
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    especialidad = models.CharField(max_length=50)
    grado_educacion = models.CharField(
        max_length=4,
        choices=GRADO_EDUCACION_CHOICES,
        default='LIC'
    )
    curriculum_vitae = models.FileField(
        upload_to='curriculums/',
        blank=True,
        null=True
    )
    horas_trabajo = models.PositiveSmallIntegerField(
        default=40,
        help_text="Horas de trabajo semanales"
    )
    fecha_contratacion = models.DateField(null=True, blank=True)
    especializaciones = models.TextField(blank=True)

    def __str__(self):
        return f"Docente: {self.usuario.get_full_name()}"

class PerfilEstudiante(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    codigo_estudiante = models.CharField(
        max_length=10,
        unique=True,
        validators=[RegexValidator(r'^[A-Z0-9]{6,10}$')]
    )
    nombre_apoderado = models.CharField(max_length=50)
    apellido_apoderado = models.CharField(max_length=50)
    promedio_general = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=0.00
    )
    grado = models.CharField(max_length=20)  # Ej: "Primero de Secundaria"
    seccion = models.CharField(max_length=1)  # Ej: "A", "B"
    alergias = models.TextField(blank=True)
    enfermedades = models.TextField(blank=True)
    telefono_apoderado = models.CharField(max_length=15)

    def __str__(self):
        return f"Estudiante: {self.usuario.get_full_name()}"

class PerfilPadre(models.Model):
    NIVEL_EDUCATIVO_CHOICES = [
        ('PRIM', 'Primaria'),
        ('SEC', 'Secundaria'),
        ('SUP', 'Superior'),
        ('TEC', 'Técnico'),
        ('POS', 'Posgrado')
    ]
    
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    ocupacion = models.CharField(max_length=50)
    nivel_educativo = models.CharField(
        max_length=4,
        choices=NIVEL_EDUCATIVO_CHOICES
    )
    direccion_trabajo = models.CharField(max_length=100, blank=True)
    telefono_trabajo = models.CharField(max_length=15, blank=True)
    parentesco = models.CharField(
        max_length=20,
        choices=[('PADRE', 'Padre'), ('MADRE', 'Madre'), ('TUTOR', 'Tutor')]
    )
    estudiantes_a_cargo = models.ManyToManyField(
        PerfilEstudiante,
        blank=True,
        related_name='tutores'
    )

    def __str__(self):
        return f"Padre/Tutor: {self.usuario.get_full_name()}"

class PerfilMedico(models.Model):
    ESPECIALIDAD_CHOICES = [
        ('PED', 'Pediatría'),
        ('PSIC', 'Psicología'),
        ('ENF', 'Enfermería'),
        ('GEN', 'Medicina General')
    ]
    
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    registro_profesional = models.CharField(max_length=50)
    especialidad = models.CharField(
        max_length=4,
        choices=ESPECIALIDAD_CHOICES
    )
    horario_atencion = models.CharField(max_length=100)
    telefono_emergencia = models.CharField(max_length=15)
    consultorio = models.CharField(max_length=20, blank=True)
    pacientes = models.ManyToManyField(
        PerfilEstudiante,
        blank=True,
        related_name='medicos'
    )

    def __str__(self):
        return f"Médico: {self.usuario.get_full_name()}"

class PerfilAdministrativo(models.Model):
    CARGO_CHOICES = [
        ('ADM', 'Administrador'),
        ('SEC', 'Secretario/a'),
        ('COO', 'Coordinador/a'),
        ('CON', 'Contador'),
        ('DIR', 'Director/a')
    ]
    
    DEPARTAMENTO_CHOICES = [
        ('ACAD', 'Académico'),
        ('ADM', 'Administración'),
        ('FIN', 'Finanzas'),
        ('MAT', 'Matrículas'),
        ('REC', 'Recursos Humanos')
    ]
    
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    cargo = models.CharField(
        max_length=3,
        choices=CARGO_CHOICES
    )
    departamento = models.CharField(
        max_length=4,
        choices=DEPARTAMENTO_CHOICES
    )
    

    def __str__(self):
        return f"Administrativo: {self.usuario.get_full_name()}"