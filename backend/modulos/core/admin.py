from django.contrib import admin
from .models import PerfilAdministrativo,PerfilDocente,PerfilEstudiante,PerfilMedico,PerfilPadreFamilia,Usuario

# Register your models here.
admin.site.register(Usuario)
admin.site.register(PerfilEstudiante)
admin.site.register(PerfilAdministrativo)
admin.site.register(PerfilDocente)
admin.site.register(PerfilPadreFamilia)
admin.site.register(PerfilMedico)
