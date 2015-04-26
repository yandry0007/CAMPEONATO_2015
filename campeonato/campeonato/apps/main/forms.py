from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from django import forms
from .models import *

class ContactoForm(forms.Form):
	correo = forms.EmailField(label='Tu correo electronico')
	mensaje = forms.CharField(widget=forms.Textarea)

class LoginForm(UserCreationForm):
	pass

# class UserForm(UserCreationForm):
# 	nombres = forms.CharField(widget=forms.TextInput())
# 	apellidos = forms.CharField(widget=forms.TextInput())
# 	cedula = forms.IntegerField()
# 	representante = forms.BooleanField()
# 	capitan = forms.BooleanField()
# 	foto = forms.ImageField(required=True)
# 	estatura = forms.CharField()
# 	correo = forms.EmailField(label='Tu correo electronico')
# 	telefono = forms.IntegerField()
	
	# def clean(self):
	# 	return self.cleaned_data


class PerfilForm(forms.ModelForm):
	class Meta:
		model = Perfiles