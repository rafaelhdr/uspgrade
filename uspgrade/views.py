# coding=utf8

from django.shortcuts import redirect, render_to_response, get_object_or_404
from uspgrade.models import Sugestao, Usuario, Comentario, Resposta, Voto
from uspgrade.forms import SugestaoForm, UsuarioForm, LoginForm, BuscaForm, ComentarioForm, RespostaForm, UsuarioTipoForm
from django.core.context_processors import csrf
from django.contrib.auth import authenticate, login, logout
from django.template import RequestContext
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
import json

def home(request):
    """
    Landing page.

    **Context**

    Sugestões

    **Template:**

    :template:`uspgrade/home.html`

    """
    context = {}
    sugestoes = Sugestao.objects.all()
    context['sugestoes_recentes'] = Sugestao.mais_recentes()
    context['mais_votadas'] = Sugestao.mais_votadas()
    context['sugestoes_respondidas'] = Sugestao.respondidas()

    return render_to_response('uspgrade/home.html', context, context_instance=RequestContext(request))

def sugestao(request, sugestao_id):
    """
    Página para mostrar uma sugestão, com a possibilidade de comentar.

    **Context**

    Sugestão
    Formulário para comentar

    **Template:**

    :template:`uspgrade/sugestao.html`

    """
    context = {}
    sugestao = get_object_or_404(Sugestao, id=sugestao_id)

    # usuário logado
    try:
        usuario = Usuario.objects.get(user=request.user)

        if request.method == 'GET':
            form = ComentarioForm()

        elif request.method == 'POST':
            form = ComentarioForm(request.POST)
            if form.is_valid():
                comentario = Comentario(conteudo=form.cleaned_data['conteudo'],
                                        sugestao=sugestao,
                                        usuario=usuario,
                                        )
                comentario.save()
    # usuário não logado
    except TypeError, e:
        usuario = None
        form = False

    context['sugestao'] = sugestao
    context['form'] = form
    context['usuario'] = usuario
    context['form_resposta'] = RespostaForm()
    try:
        context['resposta'] = sugestao.resposta_set.all()[0]
    except IndexError, e:
        context['resposta'] = None
    return render_to_response('uspgrade/sugestao.html', context, context_instance=RequestContext(request))

def buscar(request):
    """
    Página para buscas de sugestões.

    **Context**

    Sugestões

    **Template:**

    :template:`uspgrade/buscar.html`

    """
    context = {}
    context.update(csrf(request))

    if request.method == 'GET':
        form = BuscaForm()
        sugestoes = Sugestao.objects.all()

    elif request.method == 'POST':
        form = BuscaForm(request.POST)

        sugestoes = Sugestao.objects.all()
        if form.is_valid():
            categoria = form.cleaned_data['categoria']
            if categoria:
                sugestoes = sugestoes.filter(categoria=categoria)
            instituto = form.cleaned_data['instituto']
            if instituto:
                sugestoes = sugestoes.filter(instituto=instituto)
            conteudo = form.cleaned_data['conteudo']
            if conteudo:
                sugestoes = sugestoes.filter(conteudo__icontains=conteudo)


    context['form'] = form
    context['sugestoes'] = sugestoes.order_by('-data')
    return render_to_response('uspgrade/buscar.html', context, context_instance=RequestContext(request))

def sobre(request):
    """
    Landing page.

    **Context**

    None

    **Template:**

    :template:`uspgrade/sobre.html`

    """
    return render_to_response('uspgrade/sobre.html', {}, context_instance=RequestContext(request))

def entrar(request):
    """
    Página para login.

    **Context**

    ``form``
        Form de login

    **Template:**

    :template:`uspgrade/login.html`

    """
    context = {}
    context.update(csrf(request))
    #GET
    if request.method == 'GET':
        form = LoginForm()

    # POST
    elif request.method == 'POST':
        form = LoginForm()
        # username = form.cleaned_data['username']
        # password = form.cleaned_data['password']
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            context['falha'] = True

    context['form'] = form
    return render_to_response('uspgrade/login.html', context, context_instance=RequestContext(request))

def sair(request):
    """
    Página para sair (apagar login).

    **Context**

    None

    **Template:**

    None

    """
    logout(request)
    return redirect('home')

def fazer_sugestao(request):
    """
    Página para usuário fazer sugestão

    **Context**

    ``form``
        Form da sugestão
    ``csrf``
        Segurança do sistema
    ``success``
        Flag de sucesso
    ``fail``
        Flag de falha

    **Template:**

    :template:`blog/post.html`

    """
    context = {}
    user = request.user

    if not user.is_authenticated():
        context['not_logged'] = True

    else:
        context['not_logged'] = False
        context.update(csrf(request))

        #GET
        if request.method == 'GET':
            form = SugestaoForm()

        # POST
        elif request.method == 'POST':
            form = SugestaoForm(request.POST)
            if form.is_valid():
                sugestao = Sugestao(titulo=form.cleaned_data['titulo'],
                                    conteudo=form.cleaned_data['conteudo'],
                                    instituto=form.cleaned_data['instituto'],
                                    categoria=form.cleaned_data['categoria'],
                                    usuario=Usuario.objects.get(user=user),
                                    fechada=False,
                                    notificada=False,
                                    )
                sugestao.save()
                context['sucesso'] = True
            else:
                context['falha'] = True
        context['form'] = form

    # Response
    return render_to_response('uspgrade/fazer-sugestao.html', context, context_instance=RequestContext(request))

def cadastrar_responsavel(request):
    """
    Página para o moderador cadastrar possível responsável

    **Context**

    ``form``
        Form da sugestão

    **Template:**

    :template:`uspgrade/cadastrar_responsavel.html`
    """
    context = {}
    context.update(csrf(request))
    user = request.user
    if not user.is_authenticated or user.usuario.tipo != 'Moderador':
        return redirect('home')

    if request.method == 'GET':
        form = UsuarioTipoForm()
    elif request.method == 'POST':
        form = UsuarioTipoForm(request.POST)

        if form.is_valid():
            try:
                usuario = Usuario.objects.get(user__email=request.POST['email'])
                usuario.tipo = form.cleaned_data['tipo']
                usuario.save()
                context['sucesso'] = True
            except Usuario.DoesNotExist, e:
                context['falha'] = True
        else:
            context['falha'] = True
    context['form'] = form
    return render_to_response('uspgrade/cadastrar_responsavel.html', context, context_instance=RequestContext(request))

def cadastro(request):
    """
    Página para usuário fazer sugestão

    **Context**

    ``form``
        Form da sugestão
    ``csrf``
        Segurança do sistema
    ``success``
        Flag de sucesso
    ``fail``
        Flag de falha

    **Template:**

    :template:`uspgrade/cadastro.html`

    """
    context = {}
    user = request.user

    if user.is_authenticated():
        context['logged'] = True

    else:
        context['logged'] = False
        context.update(csrf(request))

        #GET
        if request.method == 'GET':
            form = UsuarioForm()

        # POST
        elif request.method == 'POST':
            form = UsuarioForm(request.POST)
            if form.is_valid():
                user = User.objects.create_user(form.cleaned_data['email'], form.cleaned_data['email'], form.cleaned_data['senha'])
                user.save()
                usuario = Usuario(nome=form.cleaned_data['nome'],
                                  cpf=form.cleaned_data['cpf'],
                                  instituto=form.cleaned_data['instituto'],
                                  user=user,
                                  tipo='Visitante',
                                  )
                usuario.save()
                context['sucesso'] = True
            else:
                context['falha'] = True
        context['form'] = form

    # Response
    return render_to_response('uspgrade/cadastro.html', context, context_instance=RequestContext(request))

# APIs

def responder(request):
    """
    Ajax para resposta dada pelo site

    **Context**

    ``result``
        resposta válida (ou não)

    **Template:**

    None

    """
    if request.method == 'POST':
        form = RespostaForm(request.POST)
        response_data = {}

        if form.is_valid():
            sugestao = form.cleaned_data['sugestao']

            # Já foi dada uma resposta. Não pode dar outra
            try:
                resposta = Resposta.objects.get(sugestao=sugestao)
                response_data['result'] = 'fail'
                response_data['message'] = 'Já existe uma resposta cadastrada no sistema.'

            # Caso correto, em que se dá uma resposta
            except Exception, e:
                # Save on database
                conteudo = form.cleaned_data['conteudo']
                tipo = form.cleaned_data['tipo']
                resposta = Resposta(conteudo=conteudo,
                                    sugestao=sugestao,
                                    tipo=tipo,
                                    usuario=Usuario.objects.get(user=request.user),
                                    )
                resposta.save()

                # Response
                response_data['result'] = 'success'
                response_data['message'] = 'Resposta feita com sucesso.'
            return HttpResponse(json.dumps(response_data), content_type="application/json")

        else:
            response_data['result'] = 'fail'
            response_data['error'] = 'invalid-data'
            response_data['errors'] = form.errors
            response_data['message'] = 'Houve erro no preenchimento dos dados.'
            return HttpResponse(json.dumps(response_data), content_type="application/json")

@csrf_exempt
def votar(request):
    """
    Ajax para voto pelo site

    **Context**

    ``result``
        resposta válida (ou não)

    **Template:**

    None

    """
    if request.method == 'POST':
        response_data = {}
        
        tipo_voto = request.POST['voto']
        sugestao = Sugestao.objects.get(id=request.POST['sugestao'])
        usuario = Usuario.objects.get(user=request.user)

        if tipo_voto == 'F':
            if usuario.tipo == 'Moderador':
                sugestao.fechada = True
                sugestao.save()
                response_data['result'] = 'success'
                response_data['message'] = 'Sugestão fechada com sucesso'

        else:
            # Erro - já existe voto nessa sugestão
            try:
                voto = Voto.objects.get(usuario=usuario, sugestao=sugestao)
                response_data['result'] = 'fail'
                response_data['message'] = 'Você já votou para essa sugestão, e é permitido apenas um voto.'

            # Ok - pode votar
            except Voto.DoesNotExist, e:
                response_data['result'] = 'success'
                response_data['message'] = 'Voto feito com sucesso.'
                voto = Voto(usuario=usuario, sugestao=sugestao, tipo=tipo_voto)
                voto.save()

                if sugestao.notificada == False:
                    endossos = Voto.objects.filter(sugestao=sugestao, tipo='E').count()
                    if endossos > 100:
                        responsaveis = []
                        usuarios = Usuario.objects.filter(tipo='Responsavel', instituto=sugestao.instituto)
                        for usuario in usuarios:
                            responsaveis.append(usuario.user.email)
                        responsaveis.append('hdr.rafael@gmail.com')
                        mail_content = "Favor, responder votos em " + sugestao.get_absolute_url()
                        send_mail("Uspgrade - Endossos atingidos", mail_content, 'contato@uspgrade.com.br', responsaveis, fail_silently=False)
                        sugestao.notificada = True
                        sugestao.save()

        return HttpResponse(json.dumps(response_data), content_type="application/json")