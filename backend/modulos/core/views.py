from django.shortcuts import render,redirect
from django.contrib.auth import login
from .forms import (RegistroAdministrativoForm, RegistroDocenteForm,RegistroEstudianteForm,RegistroMedicoForm,RegistroPadreForm,BaseRegistroForm)

# Create your views here.

def HomePage(request):
    return render(request,'core/HomePage.html')

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