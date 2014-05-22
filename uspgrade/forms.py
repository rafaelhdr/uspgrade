# coding=utf8

from django.forms import ModelForm
from django import forms
from uspgrade.models import Sugestao

class SugestaoForm(ModelForm):
    class Meta:
        model = Sugestao
        fields = ['titulo', 'conteudo', 'instituto', 'categoria']
        widgets = {
            'titulo': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Título para sua sugestão'}),
            'categoria': forms.Select(attrs={'class':'form-control'}),
            'instituto': forms.Select(attrs={'class':'form-control'}),
            'conteudo': forms.Textarea(attrs={'class':'form-control', 'placeholder': 'Conteúdo da sua sugestão'}),
        }