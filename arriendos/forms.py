from .models import Inmueble, Region, Comuna, Contact
from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from .models import Usuario, Inmueble, Region  # Importa el modelo Region
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class RegistroUsuarioForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label='Contraseña')
    confirm_password = forms.CharField(
        widget=forms.PasswordInput, label='Confirme su contraseña')

    class Meta:
        model = Usuario
        fields = ['tipo_usuario', 'rut', 'primer_nombre', 'segundo_nombre', 'primer_apellido',
                  'segundo_apellido', 'direccion', 'email', 'telefono_personal', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            self.add_error('confirm_password', "Las contraseñas no coinciden")

        return cleaned_data


class EditProfileForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label='Contraseña')
    confirm_password = forms.CharField(
        widget=forms.PasswordInput, label='Confirme su contraseña')

    class Meta:
        model = Usuario
        fields = ['tipo_usuario', 'rut', 'primer_nombre', 'segundo_nombre', 'primer_apellido',
                  'segundo_apellido', 'direccion', 'email', 'telefono_personal', 'password', 'confirm_password']

    def __init__(self, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.fields['rut'].widget.attrs['readonly'] = True
        self.fields['rut'].widget.attrs['class'] = 'form-control-plaintext'
        self.fields['primer_nombre'].widget.attrs['readonly'] = True
        self.fields['primer_nombre'].widget.attrs['class'] = 'form-control-plaintext'
        self.fields['primer_apellido'].widget.attrs['readonly'] = True
        self.fields['primer_apellido'].widget.attrs['class'] = 'form-control-plaintext'
        self.fields['email'].widget.attrs['readonly'] = True
        self.fields['email'].widget.attrs['class'] = 'form-control-plaintext'


class InmuebleForm(forms.ModelForm):
    region = forms.ModelChoiceField(
        queryset=Region.objects.all(), empty_label=None, label='Región')
    comuna = forms.ModelChoiceField(
        queryset=Comuna.objects.none(), label='Comuna')

    class Meta:
        model = Inmueble
        fields = [
            'descripcion', 'm2_construidos', 'm2_totales',
            'cantidad_estacionamientos', 'cantidad_habitaciones', 'cantidad_banos',
            'direccion', 'region', 'comuna', 'tipo_inmueble', 'precio_mensual_arriendo',
            'imagen'
        ]

    def __init__(self, *args, **kwargs):
        super(InmuebleForm, self).__init__(*args, **kwargs)
        self.fields['comuna'].queryset = Comuna.objects.none()

        if 'region' in self.data:
            try:
                region_id = int(self.data.get('region'))
                self.fields['comuna'].queryset = Comuna.objects.filter(
                    region_id=region_id).order_by('nombre')
            except (ValueError, TypeError):
                pass  # Invalid input from the client; ignore and fallback to empty Comuna queryset
        elif self.instance.pk:
            self.fields['comuna'].queryset = self.instance.region.comuna_set.order_by(
                'nombre')


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'subject', 'message']
        labels = {
            'name': 'Nombre',
            'email': 'Correo',
            'subject': 'Motivo',
            'message': 'Mensaje',
        }
