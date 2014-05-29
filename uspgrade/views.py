# coding=utf8

from django.shortcuts import redirect, render_to_response
from uspgrade.models import Sugestao, Usuario
from uspgrade.forms import SugestaoForm, UsuarioForm, LoginForm
from django.core.context_processors import csrf
from django.contrib.auth import authenticate

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
    context['sugestoes_recentes'] = sugestoes.order_by('-data')

    return render_to_response('uspgrade/home.html', context)

def sobre(request):
    """
    Landing page.

    **Context**

    None

    **Template:**

    :template:`uspgrade/sobre.html`

    """
    return render_to_response('uspgrade/sobre.html')

def login(request):
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
            context['sucesso'] = True
        else:
            context['falha'] = True

    context['form'] = form
    return render_to_response('uspgrade/login.html', context)


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
    return render_to_response('uspgrade/fazer-sugestao.html', context)

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

    :template:`blog/post.html`

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
    return render_to_response('uspgrade/cadastro.html', context)