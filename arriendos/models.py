from django import forms
from django.conf import settings
from django.db import models
from django.db.models import Model
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.exceptions import ValidationError


class UsuarioManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("El email debe ser proporcionado")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


def validar_formato_rut(value):
    if not value:
        raise ValidationError('El RUT no puede estar vacío.')
    # Verificar si el formato del RUT es válido (solo números y K, con 9 dígitos)
    if len(value) != 10 or value[8] not in '0123456789kK' or not value[:-2].isdigit():
        raise ValidationError(
            'El RUT debe tener el formato correcto: 12345678-9 o 12345678-K')


class Usuario(AbstractBaseUser, PermissionsMixin):
    TIPO = (
        ('arrendador', 'Arrendador'),
        ('arrendatario', 'Arrendatario'),
    )
    tipo_usuario = models.CharField(max_length=50, choices=TIPO)

    rut_validator = RegexValidator(
        regex=r'^\d{7,8}-[\dKk]$',
        message="El formato del RUT debe ser válido."
    )
    rut = models.CharField(max_length=10, validators=[rut_validator])

    primer_nombre = models.CharField(max_length=30)
    segundo_nombre = models.CharField(max_length=30, blank=True, null=True)
    primer_apellido = models.CharField(max_length=30)
    segundo_apellido = models.CharField(max_length=30, blank=True, null=True)
    direccion = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(unique=True)
    telefono_personal = models.CharField(max_length=9, blank=True, null=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['primer_nombre', 'primer_apellido']

    objects = UsuarioManager()

    def normalizar_rut(self):
        rut = self.rut.replace(".", "").replace("-", "")
        rut = rut[:-1] + "-" + rut[-1].upper()
        return rut

    def save(self, *args, **kwargs):
        if self.rut:
            self.rut = self.normalizar_rut()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.primer_nombre} {self.segundo_nombre} {self.primer_apellido} {self.segundo_apellido}"


class Region(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre


class Comuna(models.Model):
    nombre = models.CharField(max_length=100)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nombre} - {self.region.nombre}"


class Inmueble(models.Model):
    TIPO_INMUEBLE_CHOICES = [
        ('Casa', 'Casa'),
        ('Departamento', 'Departamento'),
        ('Parcela', 'Parcela'),
    ]
    descripcion = models.TextField()
    m2_construidos = models.PositiveIntegerField()
    m2_totales = models.PositiveIntegerField()
    cantidad_estacionamientos = models.PositiveIntegerField()
    cantidad_habitaciones = models.PositiveIntegerField()
    cantidad_banos = models.PositiveIntegerField()
    direccion = models.CharField(max_length=255)
    comuna = models.ForeignKey(Comuna, on_delete=models.CASCADE)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    tipo_inmueble = models.CharField(
        max_length=20, choices=TIPO_INMUEBLE_CHOICES)
    precio_mensual_arriendo = models.PositiveIntegerField()
    propietario = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    arrendatario = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='arrendamientos', on_delete=models.SET_NULL, null=True, blank=True)
    imagen = models.ImageField(upload_to='img', blank=True, null=True)


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=100)
    message = models.TextField()
