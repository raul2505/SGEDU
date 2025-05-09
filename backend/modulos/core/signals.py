# modulos/core/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group
from .models import (
    PerfilDocente,
    PerfilAdministrativo,
    PerfilEstudiante,
    PerfilPadreFamilia,
    PerfilMedico,
    
)

@receiver(post_save, sender=PerfilDocente)
def assign_docente_group(sender, instance, created, **kwargs):
    if created:
        group, _ = Group.objects.get_or_create(name='Docente')
        instance.usuario.groups.add(group)

@receiver(post_save, sender=PerfilAdministrativo)
def assign_administrativo_group(sender, instance, created, **kwargs):
    if created:
        group, _ = Group.objects.get_or_create(name='Administrativo')
        instance.usuario.groups.add(group)

# Añade señales para los otros perfiles
@receiver(post_save, sender=PerfilEstudiante)
def assign_estudiante_group(sender, instance, created, **kwargs):
    if created:
        group, _ = Group.objects.get_or_create(name='Estudiante')
        instance.usuario.groups.add(group)

@receiver(post_save, sender=PerfilPadreFamilia)
def assign_padre_group(sender, instance, created, **kwargs):
    if created:
        group, _ = Group.objects.get_or_create(name='Padre')
        instance.usuario.groups.add(group)

@receiver(post_save, sender=PerfilMedico)
def assign_medico_group(sender, instance, created, **kwargs):
    if created:
        group, _ = Group.objects.get_or_create(name='Medico')
        instance.usuario.groups.add(group)

#@receiver(post_save, sender=PerfilPsicologo)
#def assign_psicologo_group(sender, instance, created, **kwargs):
   # if created:
       # group, _ = Group.objects.get_or_create(name='Psicologo')
       # instance.usuario.groups.add(group)