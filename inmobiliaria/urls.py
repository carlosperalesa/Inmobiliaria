from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from arriendos.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    # index
    path('', index, name='index'),
    path('footer/', footer, name='footer'),
    path('header/', header, name='header'),
    path('welcome/', welcome, name='welcome'),
    path('contacto/', contacto, name='contacto'),

    # Manejo de inmuebles
    path('crear_inmuebles/', crear_inmuebles, name='crear_inmuebles'),
    path('ver_inmuebles/', ver_inmuebles, name='ver_inmuebles'),
    path('editar_inmuebles/<int:inmuebles_id>/',
         editar_inmuebles, name='editar_inmuebles'),
    path('ver_propiedad/<int:inmuebles_id>/',
         ver_propiedad, name='ver_propiedad'),
    path('eliminar_inmueble/<int:inmuebles_id>/',
         eliminar_inmuebles, name='eliminar_inmuebles'),
    path('eliminar_imagen/<int:imagen_id>/',
         eliminar_imagen, name='eliminar_imagen'),

    # Manejo de usuarios
    path('login/', login, name='login'),
    path('register/', register, name='register'),
    path('edit/', edit_profile, name='edit_profile'),
    path('eliminar_usuario/', eliminar_usuario, name='eliminar_usuario'),
    path('logout/', salir, name='logout'),
    # Otras rutas
    path('ajax/comunas/<int:region_id>/',
         comunas_por_region, name='comunas_por_region'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
