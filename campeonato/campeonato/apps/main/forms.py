from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from django import forms
from .models import *

class ContactoForm(forms.Form):
	correo = forms.EmailField(label='Tu correo electronico')
	mensaje = forms.CharField(widget=forms.Textarea)


class UserForm(UserCreationForm):
	pass
	#movil = forms.CharField(widget=forms.TextInput(), required=True)


class PerfilForm(forms.ModelForm):
	class Meta:
		model = Perfiles