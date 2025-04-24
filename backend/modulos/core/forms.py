from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario,PerfilDocente,PerfilEstudiante,PerfilAdministrativo,PerfilMedico,PerfilPadre

#Base para todos

class BaseRegistroForm(UserCreationForm):
    dni = forms.CharField(max_length=8)
    telefono = forms.CharField(max_length=15)
    direccion = forms.CharField(max_length=30,required=False)

    class Meta:
        model = Usuario
        fields = ['username','email','dni','telefono','direccion','password1','password2']

#Docente

class RegistroDocenteForm(BaseRegistroForm):
    especialidad = forms.CharField(max_length=20)

    def save(self,commit=True):
        usuario = super().save(commit)
        PerfilDocente.objects.create(usaurio=usuario,
                                     especialidad=self.cleaned_data['especialidad'])
        return usuario

# Estudiante
class RegistroEstudianteForm(BaseRegistroForm):
    grado = forms.CharField(max_length=10)
    seccion = forms.CharField(max_length=5)
    fecha_nacimiento = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    def save(self, commit=True):
        usuario = super().save(commit)
        PerfilEstudiante.objects.create(
            usuario=usuario,
            grado=self.cleaned_data['grado'],
            seccion=self.cleaned_data['seccion'],
            fecha_nacimiento=self.cleaned_data['fecha_nacimiento']
        )
        return usuario

# Padre/Tutor
class RegistroPadreForm(BaseRegistroForm):
    hijos = forms.ModelMultipleChoiceField(
        queryset=PerfilEstudiante.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

    def save(self, commit=True):
        usuario = super().save(commit)
        perfil_padre = PerfilPadre.objects.create(usuario=usuario)
        perfil_padre.hijos.set(self.cleaned_data['hijos'])
        return usuario

# Médico
class RegistroMedicoForm(BaseRegistroForm):
    registro_profesional = forms.CharField(max_length=50)

    def save(self, commit=True):
        usuario = super().save(commit)
        PerfilMedico.objects.create(usuario=usuario, registro_profesional=self.cleaned_data['registro_profesional'])
        return usuario

# Administrativo
class RegistroAdministrativoForm(BaseRegistroForm):
    cargo = forms.CharField(max_length=100)

    def save(self, commit=True):
        usuario = super().save(commit)
        PerfilAdministrativo.objects.create(usuario=usuario, cargo=self.cleaned_data['cargo'])
        return usuario