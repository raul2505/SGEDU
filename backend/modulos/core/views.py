from django.shortcuts import render,redirect
from django.contrib.auth import login,authenticate
from django.urls import reverse
from .forms import (RegistroAdministrativoForm, RegistroDocenteForm,RegistroEstudianteForm,RegistroMedicoForm,RegistroPadreForm,BaseRegistroForm)
from .forms import LoginForm
# Create your views here.

def HomePage(request):
    return render(request,'core/modulos_perfil/modulo_estudiante.html')

def login_view(request):
    form = LoginForm(request.POST or None)
    msg = None

    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if user:
                login(request, user)

                # Obtener el rol del usuario
                user_groups = user.groups.all()
                if user_groups.exists():
                    role = user_groups.first().name  # Toma el primer grupo asignado
                    return redirect(reverse("role_page", args=[role.lower()]))  # Redirigir a la vista según el rol

                # Si no tiene rol, redirigir a una vista por defecto
                return redirect("CreateSolicitudServicio")  

            else:
                msg = "Credenciales inválidas"
        else:
            msg = "Error al validar el formulario"

    return render(request, "Login.html", {"form": form, "msg": msg})  # Siempre retorna algo

#Registrar user

def registrar_usuario(request,FormClass,template):
    if request.method == 'POST':
        form = FormClass(request.POST)
        if form.is_valid():
            usuario = form.save()
            login(request,usuario)
            return redirect('home')
    
    else:
        form = FormClass()
    
    return render(request,template,{'form':form})

def registrar_docente(request):
    return registrar_usuario(request, RegistroDocenteForm, 'registro_docente.html')

def registrar_estudiante(request):
    return registrar_usuario(request, RegistroEstudianteForm, 'registro_estudiante.html')

def registrar_padre(request):
    return registrar_usuario(request, RegistroPadreForm, 'registro_padre.html')

def registrar_medico(request):
    return registrar_usuario(request, RegistroMedicoForm, 'registro_medico.html')

def registrar_administrativo(request):
    return registrar_usuario(request, RegistroAdministrativoForm, 'registro_administrativo.html')