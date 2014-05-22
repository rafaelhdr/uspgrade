# coding=utf8

from django.db import models
from django.contrib.auth.models import User

class Usuario(models.Model):
    """ """
    INSTITUTOS = (
       ('POLI', 'Escola Politécnica'),
       ('FEA', 'Faculdade de Economia e Administração'),
       ('ECA', 'Escola de Comunicação e Artes'),
    )
    TIPOS_USUARIOS = (
       ('Visitante', 'Visitante'),
       ('Membro', 'Membro'),
       ('Responsavel', 'Responsável'),
       ('Moderador', 'Moderador'),
    )
    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=11)
    instituto = models.CharField(max_length=50, choices=INSTITUTOS)
    tipo = models.CharField(max_length=20, choices=TIPOS_USUARIOS)
    user = models.OneToOneField(User)

class Sugestao(models.Model):
    """"""
    CATEGORIAS = (
        ('acessibilidade', 'Acessibilidade'),
        ('infraestrutura', 'Infraestrutura'),
    )
    INSTITUTOS = (
       ('POLI', 'Escola Politécnica'),
       ('FEA', 'Faculdade de Economia e Administração'),
       ('ECA', 'Escola de Comunicação e Artes'),
    )
    fechada = models.BooleanField()
    notificada = models.BooleanField()
    data = models.DateField(auto_now_add=True)
    categoria = models.CharField(max_length=30, choices=CATEGORIAS)
    titulo = models.CharField(max_length=100)
    conteudo = models.TextField()
    instituto = models.CharField(max_length=50, choices=INSTITUTOS)
    usuario = models.ForeignKey(Usuario)

class Comentario(models.Model):
    """"""
    data = models.DateField(auto_now_add=True)
    conteudo = models.TextField()
    sugestao = models.ForeignKey(Sugestao)
    usuario = models.ForeignKey(Usuario)

class Resposta(models.Model):
    """"""
    TIPO_RESPOSTA = (
        ('P', 'Positiva'),
        ('N', 'Negativa'),
    )
    data = models.DateField(auto_now_add=True)
    conteudo = models.TextField()
    tipo = models.CharField(max_length=1, choices=TIPO_RESPOSTA)
    sugestao = models.ForeignKey(Sugestao)
    usuario = models.ForeignKey(Usuario)

class Voto(models.Model):
    """"""
    TIPOS_VOTO = (
        ('D', 'Denúncia'),
        ('E', 'Endossar'),
        ('R', 'Rechaçar'),
    )
    tipo = models.CharField(max_length=1, choices=TIPOS_VOTO)
    sugestao = models.ForeignKey(Sugestao)
    usuario = models.ForeignKey(Usuario)