import os

FORMS_TEMPLATE = '''from django import forms

# Aquí puedes definir tus formularios para la app {app_name}
'''

TEMPLATE = '''from django.urls import path
from . import views


app_name = '{app_name}'

urlpatterns = [
    # path('', views.index, name='index'),
]
'''

ruta_modulos = 'modulos'
ruta_urls_config = os.path.join('config', 'urls.py')

# Validamos existencia de carpetas
if not os.path.isdir(ruta_modulos):
    print("❌ No se encontró la carpeta 'modulos/'")
    exit()

if not os.path.isfile(ruta_urls_config):
    print("❌ No se encontró 'config/urls.py'")
    exit()

# Leer el contenido actual de urls.py
with open(ruta_urls_config, 'r', encoding='utf-8') as f:
    contenido_urls_config = f.read()

# Asegurarse de que existan las importaciones necesarias
importaciones_necesarias = "from django.urls import path, include"
if importaciones_necesarias not in contenido_urls_config:
    contenido_urls_config = importaciones_necesarias + "\n" + contenido_urls_config

# Para ir agregando nuevas líneas de include()
includes_agregados = []

# Recorrer las apps en modulos
for nombre_app in os.listdir(ruta_modulos):
    ruta_app = os.path.join(ruta_modulos, nombre_app)

    if os.path.isdir(ruta_app) and '__init__.py' in os.listdir(ruta_app):
        ruta_urls = os.path.join(ruta_app, 'urls.py')

        # Crear urls.py si no existe
        if not os.path.exists(ruta_urls):
            with open(ruta_urls, 'w', encoding='utf-8') as f:
                f.write(TEMPLATE.format(app_name=nombre_app))
            print(f"✅ urls.py creado en {nombre_app}/")

        else:
            print(f"⚠️ {nombre_app}/urls.py ya existe")
        
          # Crear forms.py si no existe
        ruta_forms = os.path.join(ruta_app, 'forms.py')
        if not os.path.exists(ruta_forms):
            with open(ruta_forms, 'w', encoding='utf-8') as f:
                f.write(FORMS_TEMPLATE.format(app_name=nombre_app))
            print(f"✅ forms.py creado en {nombre_app}/")
        else:
            print(f"⚠️ {nombre_app}/forms.py ya existe")

        # Línea include a agregar
        linea_include = f"    path('{nombre_app}/', include('modulos.{nombre_app}.urls')),"
        if linea_include not in contenido_urls_config:
            includes_agregados.append(linea_include)

# Agregar nuevas líneas al final de urlpatterns
if includes_agregados:
    if 'urlpatterns = [' not in contenido_urls_config:
        print("❌ No se encontró 'urlpatterns = [' en config/urls.py")
        exit()

    nueva_lista = '\n'.join(includes_agregados)
    contenido_urls_config = contenido_urls_config.replace(
        'urlpatterns = [',
        f'urlpatterns = [\n{nueva_lista}'
    )

    # Guardar los cambios
    with open(ruta_urls_config, 'w', encoding='utf-8') as f:
        f.write(contenido_urls_config)
    print("✅ Rutas agregadas automáticamente a config/urls.py")
else:
    print("⚠️ Todas las rutas ya estaban incluidas en config/urls.py")
