from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario, PerfilDocente, PerfilEstudiante, PerfilAdministrativo, PerfilMedico, PerfilPadreFamilia,PerfilBase
import json
from django.core.validators import RegexValidator
import os
from django.conf import settings
from django.utils.translation import gettext_lazy as _

class UbicacionMixin(forms.Form):
    departamento = forms.ChoiceField(
        label=_('Departamento'),
        choices=[('', _('Seleccione departamento'))],
        required=False,
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'id_departamento'})
    )
    
    provincia = forms.ChoiceField(
        label=_('Provincia'),
        choices=[('', _('Seleccione provincia'))],
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'id_provincia',
            'disabled': 'disabled'
        })
    )
    
    distrito = forms.ChoiceField(
        label=_('Distrito'),
        choices=[('', _('Seleccione distrito'))],
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'id_distrito',
            'disabled': 'disabled'
        })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ubicacion_data = self.cargar_ubicacion_data()
        self.fields['departamento'].choices += [
            (depto['id'], depto['name']) 
            for depto in self.ubicacion_data
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Inicializa ubicacion_data con un valor por defecto vacío
        self.ubicacion_data = self.cargar_ubicacion_data() or {}

        # Cargar departamentos
        self.fields['departamento'].choices += [
            (depto['id'], depto['name']) 
            for depto in self.ubicacion_data.get('departamentos', [])
        ]
        
        # Cargar provincias (si hay datos disponibles)
        self.fields['provincia'].choices += [
            (prov['id'], prov['name']) 
            for prov in self.ubicacion_data.get('provincias', [])
        ]
        
        # Cargar distritos (si hay datos disponibles)
        self.fields['distrito'].choices += [
            (dist['id'], dist['name']) 
            for dist in self.ubicacion_data.get('distritos', [])
        ]

    def cargar_ubicacion_data(self):
    
        try:
            # Ruta a los archivos JSON
            departamentos_path = os.path.join(settings.BASE_DIR, 'static', 'data', 'departamentos.json')
            provincias_path = os.path.join(settings.BASE_DIR, 'static', 'data', 'provincias.json')
            distritos_path = os.path.join(settings.BASE_DIR, 'static', 'data', 'distritos.json')

            with open(departamentos_path, 'r', encoding='utf-8') as depto_file:
                departamentos = json.load(depto_file)
            
            with open(provincias_path, 'r', encoding='utf-8') as prov_file:
                provincias = json.load(prov_file)
            
            with open(distritos_path, 'r', encoding='utf-8') as dist_file:
                distritos = json.load(dist_file)

            # Verifica si los datos son correctos
            print("Departamentos:", departamentos)
            print("Provincias:", provincias)
            print("Distritos:", distritos)

            return {
                'departamentos': departamentos,
                'provincias': provincias,
                'distritos': distritos
            }

        except Exception as e:
            print(f"Error cargando datos de ubicación: {e}")
            return {'departamentos': [], 'provincias': [], 'distritos': []}


    def clean(self):
        cleaned_data = super().clean()
        # Validar jerarquía de ubicación
        if cleaned_data.get('distrito') and not cleaned_data.get('provincia'):
            raise forms.ValidationError(_("Seleccione una provincia para el distrito"))
        if cleaned_data.get('provincia') and not cleaned_data.get('departamento'):
            raise forms.ValidationError(_("Seleccione un departamento para la provincia"))
        return cleaned_data
    
class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control"})
    )

class PerfilBaseForm(UserCreationForm):
    
    correo_institucional = forms.EmailField(required=False)

    class Meta:
        model = Usuario
        fields = [
            'username',
            'email',
            'correo_institucional',
            'first_name',
            'last_name',
            'dni',
            'password1',
            'password2'
        ]

   

class PerfilDocenteForm(forms.ModelForm):
    class Meta:
        model = PerfilDocente
        fields = [
            'telefono',
            'direccion',
            'fecha_nacimiento',
            'genero',
            'especialidad',
            'grado_academico',
            'curriculum',
            'fecha_contratacion',
            'horas_contrato',
            'departamento',
            'provincia',
            'distrito'
        ]
        widgets = {
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'fecha_nacimiento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'genero': forms.Select(attrs={'class': 'form-control'}),
            'especialidad': forms.TextInput(attrs={'class': 'form-control'}),
            'grado_academico': forms.Select(attrs={'class': 'form-control'}),
            'fecha_contratacion': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'horas_contrato': forms.NumberInput(attrs={'class': 'form-control'}),
            'departamento':forms.Select(attrs={'class': 'form-control'}),
            'provincia':forms.Select(attrs={'class': 'form-control'}),
            'distrito':forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'grado_academico': _('Grado académico'),
            'horas_contrato': _('Horas de contrato semanales'),
        }

class PerfilEstudianteForm(forms.ModelForm,UbicacionMixin):
    class Meta:
        model = PerfilEstudiante
        fields = [
            'telefono',
            'direccion',
            'fecha_nacimiento',
            'genero',
            'codigo_estudiante',
            'grado',
            'seccion',
            'promedio_general',
            'alergias',
            'condiciones_medicas',
            'nombre_apoderado',
            'telefono_apoderado',
            'departamento',
            'provincia',
            'distrito'
        ]
        widgets = {
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'fecha_nacimiento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'genero': forms.Select(attrs={'class': 'form-control'}),
            'codigo_estudiante': forms.TextInput(attrs={'class': 'form-control'}),
            'grado': forms.Select(attrs={'class': 'form-control'}),
            'seccion': forms.TextInput(attrs={'class': 'form-control'}),
            'promedio_general': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'alergias': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'condiciones_medicas': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'nombre_apoderado': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono_apoderado': forms.TextInput(attrs={'class': 'form-control'}),
            'departamento':forms.Select(attrs={'class': 'form-control'}),
            'provincia':forms.Select(attrs={'class': 'form-control'}),
            'distrito':forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'condiciones_medicas': _('Condiciones médicas'),
        }

class PerfilPadreFamiliaForm(forms.ModelForm):
    class Meta:
        model = PerfilPadreFamilia
        fields = [
            'telefono',
            'direccion',
            'fecha_nacimiento',
            'genero',
            'ocupacion',
            'nivel_educativo',
            'parentesco',
            'direccion_trabajo',
            'telefono_trabajo',
            'estudiantes',
            'departamento',
            'provincia',
            'distrito'
        ]
        widgets = {
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'fecha_nacimiento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'genero': forms.Select(attrs={'class': 'form-control'}),
            'ocupacion': forms.TextInput(attrs={'class': 'form-control'}),
            'nivel_educativo': forms.Select(attrs={'class': 'form-control'}),
            'parentesco': forms.Select(attrs={'class': 'form-control'}),
            'direccion_trabajo': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'telefono_trabajo': forms.TextInput(attrs={'class': 'form-control'}),
            'estudiantes': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'departamento':forms.Select(attrs={'class': 'form-control'}),
            'provincia':forms.Select(attrs={'class': 'form-control'}),
            'distrito':forms.Select(attrs={'class': 'form-control'}),
        }

class PerfilMedicoForm(forms.ModelForm):
    class Meta:
        model = PerfilMedico
        fields = [
            'telefono',
            'direccion',
            'fecha_nacimiento',
            'genero',
            'registro_profesional',
            'especialidad',
            'horario_atencion',
            'telefono_emergencia',
            'consultorio',
            'pacientes',
            'departamento',
            'provincia',
            'distrito'
        ]
        widgets = {
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'fecha_nacimiento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'genero': forms.Select(attrs={'class': 'form-control'}),
            'registro_profesional': forms.TextInput(attrs={'class': 'form-control'}),
            'especialidad': forms.Select(attrs={'class': 'form-control'}),
            'horario_atencion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Ej: Lunes-Viernes 8:00-16:00')
            }),
            'telefono_emergencia': forms.TextInput(attrs={'class': 'form-control'}),
            'consultorio': forms.TextInput(attrs={'class': 'form-control'}),
            'pacientes': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'departamento':forms.Select(attrs={'class': 'form-control'}),
            'provincia':forms.Select(attrs={'class': 'form-control'}),
            'distrito':forms.Select(attrs={'class': 'form-control'}),
        }

class PerfilAdministrativoForm(forms.ModelForm):
    class Meta:
        model = PerfilAdministrativo
        fields = [
            'telefono',
            'direccion',
            'fecha_nacimiento',
            'genero',
            'cargo',
            'departamento',
            'fecha_ingreso',
            'horario_laboral',
            'departamento',
            'provincia',
            'distrito'
        ]
        widgets = {
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'fecha_nacimiento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'genero': forms.Select(attrs={'class': 'form-control'}),
            'cargo': forms.Select(attrs={'class': 'form-control'}),
            'departamento': forms.Select(attrs={'class': 'form-control'}),
            'fecha_ingreso': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'horario_laboral': forms.TextInput(attrs={'class': 'form-control'}),
            'departamento':forms.Select(attrs={'class': 'form-control'}),
            'provincia':forms.Select(attrs={'class': 'form-control'}),
            'distrito':forms.Select(attrs={'class': 'form-control'}),
        }