"""Busca dados no banco
Guarda na variável instituicoes
Envia para o template home.html"""

from django.shortcuts import render
from .models import Instituicao

def index(request):
    """Pagina principal do GuiaDoar"""

    instituicoes = Instituicao.objects.all()

    return render(request, "guiadoars/home.html", {
        "instituicoes": instituicoes
    })