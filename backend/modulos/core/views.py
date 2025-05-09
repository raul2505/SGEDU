from django.shortcuts import render,redirect
from django.contrib.auth import login,authenticate
from django.urls import reverse
from .forms import (PerfilAdministrativoForm,PerfilDocenteForm,PerfilEstudianteForm,PerfilMedicoForm,PerfilBaseForm)
from .forms import LoginForm
from django.contrib import messages
from django.shortcuts import render, redirect
from django.db import transaction  # ¡Así de simple! No necesita instalación adicional
from django.views import View
# Create your views here.

def HomePage(request):
    return render(request,'core/modulos_perfil/modulo_estudiante.html')

def docente(request):
    return render(request,'core/modulos_perfil/modulo_docente.html')

def padre(request):
    return render(request,'core/modulos_perfil/modulo_padre.html')

def personal_admi(request):
    return render(request,'core/modulos_perfil/modulo_personal_admi.html')

def personal_medico(request):
    return render(request,'core/modulos_perfil/modulo_personal_medico.html')

def personal_psicologia(request):
    return render(request,'core/modulos_perfil/modulo_personal_psicologia.html')

def login_view(request):
    form = LoginForm(request.POST or None)
    msg = None

    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                
                # Usa los nombres completos con namespace
                if hasattr(user, 'perfilestudiante'):
                    return redirect('core:home')
                elif hasattr(user, 'perfildocente'):
                    return redirect('core:docente')
                elif hasattr(user, 'perfilpadre'):
                    return redirect('core:padre')
                elif hasattr(user, 'perfiladministrativo'):
                    return redirect('core:personal_admi')
                elif hasattr(user, 'perfilmedico'):
                    return redirect('core:personal_medi')
                elif hasattr(user, 'perfilpsicologo'):
                    return redirect('core:personal_psicolo')
                else:
                    return redirect('core:padre')
            else:
                msg = "Credenciales inválidas"
        else:
            msg = "Error al validar el formulario"

    return render(request, "core/Login.html", {"form": form, "msg": msg})

class RegistroView(View):
    form_perfil_clase = None
    tipo_usuario = None
    template_name = None

    def get(self, request):
        return render(request, self.template_name, {
            'user_form': PerfilBaseForm(),
            'perfil_form': self.form_perfil_clase()
        })

    def post(self, request):
        user_form = PerfilBaseForm(request.POST)
        perfil_form = self.form_perfil_clase(request.POST, request.FILES)
        
        if user_form.is_valid() and perfil_form.is_valid():
            try:
                with transaction.atomic():
                    user = user_form.save(commit=False)
                    user.set_password(user_form.cleaned_data['password1'])
                    user.tipo_usuario = self.tipo_usuario
                    user.save()
                    
                    perfil = perfil_form.save(commit=False)
                    perfil.usuario = user
                    perfil.save()
                    perfil_form.save_m2m()
                
                messages.success(request, '¡Registro exitoso!')
                return redirect('login')
            
            except Exception as e:
                messages.error(request, f'Error: {str(e)}')
        else:
            self._handle_errors(user_form, perfil_form)
        
        return render(request, self.template_name, {
            'user_form': user_form,
            'perfil_form': perfil_form
        })

    def _handle_errors(self, user_form, perfil_form):
        for form, prefix in [(user_form, 'Usuario'), (perfil_form, 'Perfil')]:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(self.request, f'{prefix}: {field} - {error}')

class RegistroAlumnoView(RegistroView):
    form_perfil_clase = PerfilEstudianteForm
    tipo_usuario = 'ESTUDIANTE'
    template_name = 'core/Registros/registro_estudiante.html'

class RegistroDocenteView(RegistroView):
    form_perfil_clase = PerfilDocenteForm
    tipo_usuario = 'DOCENTE'
    template_name = 'core/Registros/registro_docente.html'

class RegistroMedicoView(RegistroView):
    form_perfil_clase = PerfilMedicoForm
    tipo_usuario = 'MEDICO'
    template_name = 'core/Registros/registro_medico.html'

class RegistroAdministrativoView(RegistroView):
    form_perfil_clase = PerfilAdministrativoForm
    tipo_usuario = 'ADMINISTRATIVO'
    template_name = 'core/Registros/registro_administrativo.html'
#def registrar_docente(request):
   # return registrar_usuario(request, RegistroDocenteForm, 'registro_docente.html')

#def registrar_estudiante(request):
    #return registrar_usuario(request, RegistroEstudianteForm, 'registro_estudiante.html')

#def registrar_padre(request):
    #return registrar_usuario(request, RegistroPadreForm, 'registro_padre.html')

#def registrar_medico(request):
    #return registrar_usuario(request, RegistroMedicoForm, 'registro_medico.html')

#def registrar_administrativo(request):
    #return registrar_usuario(request, RegistroAdministrativoForm, 'registro_administrativo.html')