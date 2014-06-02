# coding=utf8

from django.db import models
from django.db.models import Count
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

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

    def __unicode__(self):
        """Display nome as instance information"""
        return self.nome

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
    data = models.DateTimeField(auto_now_add=True)
    categoria = models.CharField(max_length=30, choices=CATEGORIAS)
    titulo = models.CharField(max_length=100)
    conteudo = models.TextField()
    instituto = models.CharField(max_length=50, choices=INSTITUTOS)
    usuario = models.ForeignKey(Usuario)

    @classmethod
    def mais_recentes(cls):
        return cls.objects.order_by('-data')[0:10]

    @classmethod
    def mais_votadas(cls):
        votos = Voto.objects.values('sugestao__titulo').annotate(qntd_votos=Count('sugestao')).order_by('-qntd_votos')[0:10]
        return votos
        sugestoes = []
        for voto in votos:
            pass
            #sugestoes.append(voto.sugestao)
        return sugestoes

    @classmethod
    def respondidas(cls):
        respostas = Resposta.objects.order_by('pk').select_related('sugestao')[0:10]
        sugestoes = []
        for resposta in respostas:
            sugestoes.append(resposta.sugestao)
        return sugestoes

    def __unicode__(self):
        """Display titulo as instance information"""
        return self.titulo

    def get_absolute_url(self):
        return reverse('sugestao', args=[str(self.id)])

    def get_comentarios(self):
        return self.comentario_set.all().order_by('-pk')

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