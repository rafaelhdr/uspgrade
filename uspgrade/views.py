# coding=utf8

from django.shortcuts import redirect, render_to_response

def home(request):
    """
    Landing page.

    **Context**

    Sugestões

    **Template:**

    :template:`uspgrade/home.html`

    """
    return render_to_response('uspgrade/home.html')