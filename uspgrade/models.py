# coding=utf8

from django.db import models

class Usuario(models.Model):
    """ """
	INSTITUTOS = (
	   ('POLI', 'Escola Politécnica'),
	   ('FEA', 'Faculdade de Economia e Administração'),
	   ('ECA', 'Escola de Comunicação e Artes'),
	)
	TIPOS = (
	   ('Visitante', 'Visitante'),
	   ('Membro', 'Membro'),
	   ('Responsavel', 'Responsável'),
	   ('Moderador', 'Moderador'),
	)
	nome = models.CharField(max_lenght=100)
	cpf = models.CharField(max_lenght=11)
	instituto = models.CharField(max_lenght=50, choices=INSTITUTOS)
	tipo = models.CharField(max_lenght=20, choices=TIPOS)