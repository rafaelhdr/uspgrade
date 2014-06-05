# coding=utf8

from django.test import TestCase
from django.test.client import Client
from uspgrade.models import Usuario, Sugestao, Voto, Comentario, Resposta

class UspgradeTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_cadastra_usuario_com_sucesso(self):
        """
        
        """
        response = self.client.post('/cadastro',
                                    {'nome': 'Novo usuário',
                                     'cpf': '1234567890',
                                     'email': 'teste@uspgrade.com.br',
                                     'senha': 'minha-senha',
                                     'instituto': 'POLI',
                                    })

        # Check post was inserted and is not active
        usuario = Usuario.objects.get(nome='Novo usuário')
        self.assertEqual(usuario.cpf, '1234567890')
        self.assertEqual(usuario.instituto, 'POLI')
        self.assertEqual(usuario.user.email, 'teste@uspgrade.com.br')

    def test_cadastro_de_usuario_falha_caso_seja_preenchido_com_dados_incorretos(self):
        """
        
        """
        response = self.client.post('/cadastro',
                                    {'nome': 'Novo usuário',
                                     'cpf': '',
                                     'email': '',
                                     'senha': '',
                                     'instituto': '',
                                    })
        self.assertEqual(response.context['falha'], True)

    def test_usuario_consegue_fazer_login_no_sistema(self):
        """
        
        """
        response = self.client.post('/login',
                                    {'username': 'rafael',
                                     'password': 'asdasd',
                                    })
        self.assertRedirects(response, '/')

    def test_usuario_recebe_erro_caso_preencha_login_incorretamente(self):
        """
        
        """
        response = self.client.post('/login',
                                    {'username': 'rafael',
                                     'password': 'senha-incorreta',
                                    })
        self.assertEqual(response.context['falha'], True)

    def test_usuario_consegue_fazer_logout_do_sistema(self):
        """
        
        """
        response = self.client.post('/login',
                                    {'username': 'rafael',
                                     'password': 'asdasd',
                                    })
        response = self.client.get('/fazer-sugestao')
        self.assertEqual(response.context['not_logged'], False)

        response = self.client.get('/sair')
        response = self.client.get('/fazer-sugestao')
        self.assertEqual(response.context['not_logged'], True)


    def test_usuario_logado_consegue_cadastrar_sugestao_com_sucesso(self):
        """
        
        """
        response = self.client.post('/login',
                                    {'username': 'rafael',
                                     'password': 'asdasd',
                                    })

        response = self.client.post('/fazer-sugestao',
                                    {'titulo': 'Titulo de minha sugestao',
                                     'conteudo': 'Conteudo de minha sugestao',
                                     'instituto': 'POLI',
                                     'categoria': 'acessibilidade',
                                    })
        sugestao = Sugestao.objects.get(titulo='Titulo de minha sugestao')
        self.assertEqual(sugestao.titulo, 'Titulo de minha sugestao')
        self.assertEqual(sugestao.conteudo, 'Conteudo de minha sugestao')
        self.assertEqual(sugestao.instituto, 'POLI')
        self.assertEqual(sugestao.categoria, 'acessibilidade')

    def test_usuario_consegue_votar_sugestao_e_atualiza_score_correto(self):
        """
        
        """
        response = self.client.post('/login',
                                    {'username': 'rafael',
                                     'password': 'asdasd',
                                    })
        response = self.client.post('/api/votar',
                                   {'voto': 'E',
                                    'sugestao': '1',
                                   })
        usuario = Usuario.objects.get(pk=1)
        sugestao = Sugestao.objects.get(pk=1)
        voto = Voto.objects.get(usuario=usuario, tipo='E', sugestao=sugestao)
        self.assertEqual(voto.tipo, 'E')

    def test_usuario_consegue_comentar_sugestao(self):
        """
        
        """
        response = self.client.post('/login',
                                    {'username': 'rafael',
                                     'password': 'asdasd',
                                    })
        response = self.client.post('/sugestao/1',
                                   {'conteudo': 'Conteudo de meu comentario',
                                   })
        usuario = Usuario.objects.get(pk=1)
        comentario = Comentario.objects.get(conteudo='Conteudo de meu comentario', usuario=usuario)
        self.assertEqual(comentario.conteudo, 'Conteudo de meu comentario')
        self.assertEqual(comentario.usuario, usuario)

    def test_usuario_consegue_buscar_sugestoes(self):
        """
        
        """
        response = self.client.post('/buscar',
                                   {'categoria': 'infraestrutura',
                                   })
        for sugestao in response.context['sugestoes']:
            self.assertEqual(sugestao.categoria, 'infraestrutura')

    def test_visitante_consegue_abrir_pagina_de_sugestao(self):
        """
        
        """
        response = self.client.get('/sugestao/1')
        sugestao = response.context['sugestao']

        self.assertEqual(sugestao.categoria, 'acessibilidade')
        self.assertEqual(sugestao.instituto, 'POLI')

    def test_responsavel_pode_responder_sugestao(self):
        """
        
        """
        response = self.client.post('/login',
                                    {'username': 'rafael',
                                     'password': 'asdasd',
                                    })
        response = self.client.post('/api/responder',
                                   {'conteudo': 'Resposta da sugestao',
                                    'sugestao': '1',
                                    'tipo': 'P',
                                   })
        usuario = Usuario.objects.get(pk=1)
        resposta = Resposta.objects.get(usuario=usuario, conteudo='Resposta da sugestao')
        self.assertEqual(resposta.conteudo, 'Resposta da sugestao')

    def test_moderador_pode_cadastrar_responsavel(self):
        """
        
        """
        response = self.client.post('/login',
                                    {'username': 'rafael',
                                     'password': 'asdasd',
                                    })
        response = self.client.post('/cadastrar-responsavel',
                                   {'tipo': 'Membro',
                                    'email': 'rafael@hurpia.com.br'
                                   })
        usuario = Usuario.objects.get(pk=1)
        self.assertEqual(usuario.tipo, 'Membro')

    def test_moderador_pode_fechar_sugestao(self):
        """
        
        """
        response = self.client.post('/login',
                                    {'username': 'rafael',
                                     'password': 'asdasd',
                                    })
        response = self.client.post('/api/votar',
                                   {'voto': 'F',
                                    'sugestao': '1',
                                   })
        sugestao = Sugestao.objects.get(pk=1)
        self.assertEqual(sugestao.fechada, True)

    def test_sistema_envia_email_para_responsavel_quando_sugestao_atinge_x_votos(self):
        """
        
        """
        usuario = Usuario.objects.get(pk=2)
        sugestao = Sugestao.objects.get(pk=1)
        for i in range(100):
            voto = Voto(usuario=usuario, sugestao=sugestao, tipo='E')
            voto.save()
        response = self.client.post('/login',
                                    {'username': 'rafael',
                                     'password': 'asdasd',
                                    })
        response = self.client.post('/api/votar',
                                   {'voto': 'E',
                                    'sugestao': '1',
                                   })
        sugestao = Sugestao.objects.get(pk=1)
        self.assertEqual(sugestao.notificada, True)
