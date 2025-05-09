from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator, FileExtensionValidator
from django.utils.translation import gettext_lazy as _

class Usuario(AbstractUser):
    """
    Modelo de usuario minimalista que hereda de AbstractUser.
    Contiene solo los campos esenciales para autenticación y identificación básica.
    """
    dni = models.CharField(
        _('DNI'),
        max_length=8,
        unique=True,
        validators=[RegexValidator(r'^\d+$', _('Solo números permitidos.'))],
        help_text=_('Documento Nacional de Identidad (8 dígitos)')
    )
    
    foto_perfil = models.ImageField(
        _('Foto de perfil'),
        upload_to='usuarios/fotos/',
        default='usuarios/fotos/default.png',
        blank=True
    )
    
    # Campos básicos que ya incluye AbstractUser:
    # username, first_name, last_name, email, is_staff, is_active, date_joined, etc.
    
    class Meta:
        verbose_name = _('Usuario')
        verbose_name_plural = _('Usuarios')
        ordering = ['last_name', 'first_name']
    
    def __str__(self):
        return self.get_full_name() or self.username
    
    def get_short_name(self):
        """Devuelve el nombre corto del usuario."""
        return self.first_name
    
    def get_full_name(self):
        """Devuelve el nombre completo del usuario."""
        return f"{self.first_name} {self.last_name}".strip()


class PerfilBase(models.Model):
    """
    Modelo abstracto base para todos los perfiles.
    Contiene campos comunes a todos los perfiles de usuario.
    """
    usuario = models.OneToOneField(
        Usuario,
        on_delete=models.CASCADE,
        related_name='%(class)s'
    )
    
    telefono = models.CharField(
        _('Teléfono'),
        max_length=15,
        validators=[RegexValidator(r'^\+?\d{9,15}$', _('Formato: +[código][número]'))],
        blank=True
    )
    
    direccion = models.TextField(
        _('Dirección'),
        blank=True
    )
    
    fecha_nacimiento = models.DateField(
        _('Fecha de nacimiento'),
        null=True,
        blank=True
    )
    
    GENERO_CHOICES = [
        ('M', _('Masculino')),
        ('F', _('Femenino')),
        ('O', _('Otro')),
        ('N', _('Prefiero no decir'))
    ]
    
    genero = models.CharField(
        _('Género'),
        max_length=1,
        choices=GENERO_CHOICES,
        blank=True
    )
    
    creado = models.DateTimeField(auto_now_add=True)

    actualizado = models.DateTimeField(auto_now=True)
    
    departamento = models.CharField(
        _('Departamento'),
        max_length=50,
        blank=True
    )
    
    provincia = models.CharField(
        _('Provincia'),
        max_length=50,
        blank=True
    )
    
    distrito = models.CharField(
        _('Distrito'),
        max_length=50,
        blank=True
    )
    
    class Meta:
        abstract = True
    
    def __str__(self):
        return f"{self.usuario.get_full_name()} ({self.get_tipo_perfil()})"
    
    def get_tipo_perfil(self):
        return self._meta.verbose_name


class PerfilDocente(PerfilBase):
    """
    Perfil específico para docentes.
    """
    GRADO_ACADEMICO_CHOICES = [
        ('BACH', _('Bachiller')),
        ('LIC', _('Licenciado')),
        ('MG', _('Magíster')),
        ('DR', _('Doctor')),
        ('OTRO', _('Otro'))
    ]
    
    especialidad = models.CharField(
        _('Especialidad'),
        max_length=100
    )
    
    grado_academico = models.CharField(
        _('Grado académico'),
        max_length=4,
        choices=GRADO_ACADEMICO_CHOICES,
        default='LIC'
    )
    
    curriculum = models.FileField(
        _('Currículum Vitae'),
        upload_to='docentes/curriculums/',
        validators=[
            FileExtensionValidator(['pdf', 'doc', 'docx']),
            # Aquí podrías añadir validadores de tamaño máximo
        ],
        blank=True,
        null=True
    )
    
    fecha_contratacion = models.DateField(
        _('Fecha de contratación'),
        null=True,
        blank=True
    )
    
    horas_contrato = models.PositiveSmallIntegerField(
        _('Horas de contrato semanales'),
        default=40
    )
    
    activo = models.BooleanField(
        _('Activo'),
        default=True
    )
    
    class Meta:
        verbose_name = _('Perfil de docente')
        verbose_name_plural = _('Perfiles de docentes')


class PerfilEstudiante(PerfilBase):
    """
    Perfil específico para estudiantes.
    """
    codigo_estudiante = models.CharField(
        _('Código de estudiante'),
        max_length=10,
        unique=True,
        validators=[RegexValidator(r'^[A-Z0-9]{6,10}$', _('Formato inválido'))]
    )
    
    GRADO_CHOICES = [
        ('1PRIM', _('Primero de Primaria')),
        ('2PRIM', _('Segundo de Primaria')),
        ('3PRIM', _('Tercero de Primaria')),
        ('4PRIM', _('Cuarto de Primaria')),
        ('5PRIM', _('Quinto de Primaria')),
        ('6PRIM', _('Sexto de Primaria')),
        ('1SEC', _('Primero de Secundaria')),
        ('2SEC', _('Segundo de Secundaria')),
        ('3SEC', _('Tercero de Secundaria')),
        ('4SEC', _('Cuarto de Secundaria')),
        ('5SEC', _('Quinto de Secundaria')),
        
    ]
    
    grado = models.CharField(
        _('Grado'),
        max_length=5,
        choices=GRADO_CHOICES
    )
    
    seccion = models.CharField(
        _('Sección'),
        max_length=1,
        default='A'
    )
    
    promedio_general = models.DecimalField(
        _('Promedio general'),
        max_digits=4,
        decimal_places=2,
        default=0.00
    )
    
    alergias = models.TextField(
        _('Alergias conocidas'),
        blank=True
    )
    
    condiciones_medicas = models.TextField(
        _('Condiciones médicas'),
        blank=True
    )
    
    nombre_apoderado = models.CharField(
        _('Nombre del apoderado'),
        max_length=100
    )
    
    telefono_apoderado = models.CharField(
        _('Teléfono del apoderado'),
        max_length=15
    )
    
    class Meta:
        verbose_name = _('Perfil de estudiante')
        verbose_name_plural = _('Perfiles de estudiantes')


class PerfilPadreFamilia(PerfilBase):
    """
    Perfil específico para padres de familia o tutores.
    """
    NIVEL_EDUCATIVO_CHOICES = [
        ('PRIM', _('Primaria')),
        ('SEC', _('Secundaria')),
        ('SUP', _('Superior')),
        ('TEC', _('Técnico')),
        ('POS', _('Posgrado'))
    ]
    
    PARENTESCO_CHOICES = [
        ('PADRE', _('Padre')),
        ('MADRE', _('Madre')),
        ('TUTOR', _('Tutor legal')),
        ('OTRO', _('Otro'))
    ]
    
    ocupacion = models.CharField(
        _('Ocupación'),
        max_length=100
    )
    
    nivel_educativo = models.CharField(
        _('Nivel educativo'),
        max_length=4,
        choices=NIVEL_EDUCATIVO_CHOICES
    )
    
    parentesco = models.CharField(
        _('Parentesco'),
        max_length=5,
        choices=PARENTESCO_CHOICES
    )
    
    direccion_trabajo = models.TextField(
        _('Dirección de trabajo'),
        blank=True
    )
    
    telefono_trabajo = models.CharField(
        _('Teléfono de trabajo'),
        max_length=15,
        blank=True
    )
    
    estudiantes = models.ManyToManyField(
        PerfilEstudiante,
        related_name='padres',
        verbose_name=_('Estudiantes a cargo'),
        blank=True
    )
    
    class Meta:
        verbose_name = _('Perfil de padre/tutor')
        verbose_name_plural = _('Perfiles de padres/tutores')


class PerfilAdministrativo(PerfilBase):
    """
    Perfil específico para personal administrativo.
    """
    CARGO_CHOICES = [
        ('ADM', _('Administrador')),
        ('SEC', _('Secretario/a')),
        ('COO', _('Coordinador/a')),
        ('CON', _('Contador')),
        ('DIR', _('Director/a'))
    ]
    
    DEPARTAMENTO_CHOICES = [
        ('ACAD', _('Académico')),
        ('ADM', _('Administración')),
        ('FIN', _('Finanzas')),
        ('MAT', _('Matrículas')),
        ('REC', _('Recursos Humanos'))
    ]
    
    cargo = models.CharField(
        _('Cargo'),
        max_length=3,
        choices=CARGO_CHOICES
    )
    
    departamento = models.CharField(
        _('Departamento'),
        max_length=4,
        choices=DEPARTAMENTO_CHOICES
    )
    
    fecha_ingreso = models.DateField(
        _('Fecha de ingreso'),
        null=True,
        blank=True
    )
    
    horario_laboral = models.CharField(
        _('Horario laboral'),
        max_length=100,
        blank=True
    )
    
    class Meta:
        verbose_name = _('Perfil administrativo')
        verbose_name_plural = _('Perfiles administrativos')


class PerfilMedico(PerfilBase):
    """
    Perfil específico para personal médico.
    """
    ESPECIALIDAD_CHOICES = [
        ('PED', _('Pediatría')),
        ('PSIC', _('Psicología')),
        ('ENF', _('Enfermería')),
        ('GEN', _('Medicina General'))
    ]
    
    registro_profesional = models.CharField(
        _('Registro profesional'),
        max_length=50,
        unique=True
    )
    
    especialidad = models.CharField(
        _('Especialidad'),
        max_length=4,
        choices=ESPECIALIDAD_CHOICES
    )
    
    horario_atencion = models.CharField(
        _('Horario de atención'),
        max_length=100
    )
    
    telefono_emergencia = models.CharField(
        _('Teléfono de emergencia'),
        max_length=15
    )
    
    consultorio = models.CharField(
        _('Consultorio'),
        max_length=20,
        blank=True
    )
    
    pacientes = models.ManyToManyField(
        PerfilEstudiante,
        related_name='medicos',
        verbose_name=_('Pacientes a cargo'),
        blank=True
    )
    
    class Meta:
        verbose_name = _('Perfil médico')
        verbose_name_plural = _('Perfiles médicos')