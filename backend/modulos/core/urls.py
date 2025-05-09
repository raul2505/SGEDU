from django.urls import path
from . import views

app_name = 'core'


urlpatterns = [
    path('', views.HomePage, name='home'),
    path('Login/',views.login_view,name='Login'),

    path('docente/',views.docente,name='docente'),
    path('padre/',views.padre,name='padre'),
    path('personal_admi/',views.personal_admi,name='personal_admi'),
    path('personal_medi/',views.personal_medico,name='personal_medi'),
    path('personal_psico/',views.personal_psicologia,name='personal_psicolo'),

#REGISTROS DE USUARIOS 
    path('registro_alumno/',views.RegistroAlumnoView.as_view(),name='registro_alumno'),
    path('registro_docente/',views.RegistroDocenteView.as_view(),name='registro_docente'),
    path('registro_personal_medico/',views.RegistroMedicoView.as_view(),name='registro_personal_medico'),
    path('registro_personal_admi/',views.RegistroAdministrativoView.as_view() ,name='registro_personal_admi'),

]
