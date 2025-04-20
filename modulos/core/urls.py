from django.urls import path
from . import views

app_name = 'core'


urlpatterns = [
    path('edu', views.HomePage, name='home'),
]
