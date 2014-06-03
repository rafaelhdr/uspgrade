# coding=utf8

from django.forms import ModelForm
from django import forms
from uspgrade.models import Sugestao, Usuario, Comentario, Resposta
from django.contrib.auth.models import User

class ComentarioForm(ModelForm):
    class Meta:
        model = Comentario
        fields = ['conteudo',]
        widgets = {
            'conteudo': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Escreva aqui seu comentário'}),
        }

class BuscaForm(ModelForm):
    class Meta:
        model = Sugestao
        fields = ['conteudo', 'instituto', 'categoria']
        widgets = {
            'conteudo': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Conteúdo da sua sugestão'}),
            'categoria': forms.Select(attrs={'class':'form-control'}),
            'instituto': forms.Select(attrs={'class':'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(BuscaForm, self).__init__(*args, **kwargs)
        self.fields['conteudo'].required = False
        self.fields['categoria'].required = False
        self.fields['instituto'].required = False

class RespostaForm(ModelForm):
    class Meta:
        model = Resposta
        fields = ['tipo', 'sugestao', 'conteudo']
        widgets = {
            'tipo': forms.Select(attrs={'class':'form-control'}),
            'sugestao': forms.HiddenInput(),
            'conteudo': forms.Textarea(attrs={'class':'form-control', 'placeholder': 'Resposta para os usuários'}),
        }

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

class LoginForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Seu e-mail'}),
            'password': forms.PasswordInput(attrs={'class':'form-control', 'placeholder': 'Sua senha'}),
        }

class UsuarioForm(ModelForm):
    senha = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder': 'Senha'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'e-mail'}))
    class Meta:
        model = Usuario
        fields = ['nome', 'cpf', 'email', 'senha', 'instituto']
        widgets = {
            'nome': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Seu nome completo'}),
            'cpf': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'CPF'}),
            'instituto': forms.Select(attrs={'class':'form-control'}),
        }
