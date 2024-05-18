from .forms import ContactForm, RegistroUsuarioForm, EditProfileForm, InmuebleForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.hashers import make_password
from django.contrib.auth import logout, authenticate, login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse_lazy

# Create your views here.


def index(request):
    return render(request, 'welcome.html')


def welcome(request):
    return render(request, 'welcome.html')


def footer(request):
    return render(request, 'footer.html')


def header(request):
    return render(request, 'header.html')


def register(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data['password']
            user.password = make_password(password)
            user.save()
            messages.success(
                request, 'Tu registro se ha completado con éxito. ¡Bienvenido a la comunidad!')
            return redirect('login')
        else:
            messages.error(
                request, 'Hubo un problema con tu registro. Por favor, intenta de nuevo.')
    else:
        form = RegistroUsuarioForm()
    return render(request, 'registration/register.html', {'form': form})


def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('index')
            else:
                messages.error(
                    request, 'Credenciales inválidas. Por favor, intenta de nuevo.')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data.get('password')
            if password:
                user.set_password(password)
            user.save()

            # Verificar si se solicitó eliminar el perfil
            if "eliminar_perfil" in request.POST:
                # Eliminar el perfil
                request.user.delete()
                # Desconectar al usuario
                logout(request)
                # Redirigir a la página de inicio
                return HttpResponseRedirect(reverse_lazy("index"))
            else:
                messages.success(request, 'Perfil actualizado correctamente.')
                return redirect('edit_profile')
        else:
            messages.error(
                request, 'Hubo un problema al actualizar el perfil.')
    else:
        form = EditProfileForm(instance=request.user)
    return render(request, 'registration/edit.html', {'form': form})


@login_required
def eliminar_usuario(request):
    if request.method == 'POST':
        request.user.delete()
        messages.success(request, 'Tu perfil ha sido eliminado correctamente.')
        return redirect('index')
    else:
        return HttpResponse("Error: Método no permitido", status=405)


@login_required
def salir(request):
    logout(request)
    return redirect('index')


def comunas_por_region(request, region_id):
    comunas = Comuna.objects.filter(region_id=region_id).values('id', 'nombre')
    return JsonResponse(list(comunas), safe=False)


@login_required
def crear_inmuebles(request):
    if request.method == 'POST':
        form = InmuebleForm(request.POST, request.FILES)
        if form.is_valid():
            inmueble = form.save(commit=False)
            inmueble.propietario = request.user
            inmueble.save()
            messages.success(request, 'Inmueble creado con éxito.')
            return redirect('ver_inmuebles')
    else:
        form = InmuebleForm()
    return render(request, 'inmuebles/crear_inmuebles.html', {'form': form})


@login_required  # vista general
def ver_inmuebles(request):
    inmuebles = Inmueble.objects.all()
    regiones = Region.objects.all()
    comunas = Comuna.objects.all()
    return render(request, 'inmuebles/ver_inmuebles.html', {'regiones': regiones, 'comunas': comunas, 'inmuebles': inmuebles})


def ver_propiedad(request, inmuebles_id):
    print("Entrando a la vista ver_propiedad")  # Agregar este print
    inmueble = get_object_or_404(Inmueble, id=inmuebles_id)
    return render(request, 'inmuebles/ver_propiedad.html', {'inmueble': inmueble})


@login_required
def editar_inmuebles(request, inmuebles_id):
    inmueble = get_object_or_404(Inmueble, id=inmuebles_id)
    if request.user.tipo_usuario != 'arrendador' or request.user != inmueble.propietario:
        return redirect('ver_inmuebles')

    if request.method == 'POST':
        form = InmuebleForm(request.POST, instance=inmueble)
        if form.is_valid():
            form.save()
            messages.success(request, 'Inmueble actualizado con éxito.')
            return render(request, 'inmuebles/editar_inmuebles.html', {'form': form, 'inmueble': inmueble, 'form_submitted': True})
        else:
            messages.error(
                request, 'Hubo un problema al actualizar el inmueble.')
    else:
        form = InmuebleForm(instance=inmueble)

    return render(request, 'inmuebles/editar_inmuebles.html', {'form': form, 'inmueble': inmueble})


@login_required
def eliminar_inmuebles(request, inmuebles_id):
    inmueble = get_object_or_404(Inmueble, id=inmuebles_id)
    if request.user.tipo_usuario == 'arrendador' and request.user == inmueble.propietario:
        inmueble.delete()
        messages.success(request, 'Inmueble eliminado con éxito')
    return redirect('ver_inmuebles')


def contacto(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            form_submitted = True
        else:
            form_submitted = False
    else:
        form_submitted = False
        # Prefill the form with GET parameters
        initial_data = {
            'name': request.GET.get('name', ''),
            'email': request.GET.get('email', ''),
            'subject': request.GET.get('subject', ''),
            'message': request.GET.get('message', '')
        }
        form = ContactForm(initial=initial_data)

    return render(request, 'contacto.html', {'form': form, 'form_submitted': form_submitted})
