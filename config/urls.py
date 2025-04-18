from django.urls import path, include
"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('academico/', include('modulos.academico.urls')),
    path('admision/', include('modulos.admision.urls')),
    path('agenda/', include('modulos.agenda.urls')),
    path('biblioteca/', include('modulos.biblioteca.urls')),
    path('clases/', include('modulos.clases.urls')),
    path('core/', include('modulos.core.urls')),
    path('historico/', include('modulos.historico.urls')),
    path('intranet/', include('modulos.intranet.urls')),
    path('medico/', include('modulos.medico.urls')),
    path("admin/", admin.site.urls),
]
