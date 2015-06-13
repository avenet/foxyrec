from django import forms
from .models import *


class UsuarioForm(forms.ModelForm):
    sexo = forms.ChoiceField(
        required=True,
        choices=Usuario.SEXO,
        widget=forms.Select(attrs={'class': 'input-field'})
    )
    edad = forms.ChoiceField(
        required=True,
        choices=Usuario.RANGO_ETAREO,
        widget=forms.Select(attrs={'class': 'input-field'})
    )

    class Meta:
        model = Usuario
        fields = ['sexo', 'edad']


class SeleccionForm(forms.ModelForm):
    usuario = forms.CharField(widget=forms.HiddenInput())
    item = forms.CharField(widget=forms.HiddenInput())

    class Meta:
        model = Seleccion
        fields = ['usuario', 'item', 'me_gusta']
        exclude = ('usuario', 'item', 'me_gusta',)
