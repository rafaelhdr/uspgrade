# coding=utf8

from django.shortcuts import redirect, render_to_response
from uspgrade.models import Sugestao

def home(request):
    """
    Landing page.

    **Context**

    Sugestões

    **Template:**

    :template:`uspgrade/home.html`

    """
    context = {}
    context['sugestoes'] = Sugestao.objects.all()

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
