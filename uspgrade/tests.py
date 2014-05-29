# coding=utf8

from django.test import TestCase
from django.test.client import Client

class UspgradeTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_cadastra_usuario_com_sucesso(self):
        """
        
        """
        response = self.client.get('/')

    def test_cadastro_de_usuario_falha_caso_seja_preenchido_com_dados_incorretos(self):
        """
        
        """
        response = self.client.get('/')

    def test_usuario_consegue_fazer_login_no_sistema(self):
        """
        
        """
        response = self.client.get('/')

    def test_usuario_recebe_erro_caso_preencha_login_incorretamente(self):
        """
        
        """
        response = self.client.get('/')

    def test_usuario_consegue_fazer_logout_do_sistema(self):
        """
        
        """
        response = self.client.get('/')

    def test_usuario_logado_consegue_cadastrar_sugestao_com_sucesso(self):
        """
        
        """
        response = self.client.get('/')

    def test_usuario_consegue_votar_sugestao_e_atualiza_score_correto(self):
        """
        
        """
        response = self.client.get('/')

    def test_usuario_consegue_comentar_sugestao(self):
        """
        
        """
        response = self.client.get('/')

    def test_usuario_consegue_buscar_sugestoes(self):
        """
        
        """
        response = self.client.get('/')

    def test_visitante_consegue_abrir_pagina_de_sugestao(self):
        """
        
        """
        response = self.client.get('/')

    def test_responsavel_pode_responder_sugestao(self):
        """
        
        """
        response = self.client.get('/')

    def test_moderador_pode_cadastrar_responsavel(self):
        """
        
        """
        response = self.client.get('/')

    def test_moderador_pode_fechar_sugestao(self):
        """
        
        """
        response = self.client.get('/')

    def test_sistema_envia_email_para_responsavel_quando_sugestao_atinge_x_votos(self):
        """
        
        """
        response = self.client.get('/')