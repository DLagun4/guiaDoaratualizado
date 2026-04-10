"""Busca dados no banco
Guarda na variável instituicoes
Envia para o template home.html"""

from django.shortcuts import render
from .models import Instituicao, CategoriaDoacao
from .models import Instituicao

def index(request):
    """Página principal do GuiaDoar com busca por categoria e cidade"""

    cidade = request.GET.get('cidade', '').strip()
    categoria_nome = request.GET.get('tipo', '').strip()

    instituicoes = Instituicao.objects.filter(ativa=True)

    if cidade:
        instituicoes = instituicoes.filter(cidade__icontains=cidade)

    if categoria_nome:
        instituicoes = instituicoes.filter(categorias_doacao__nome__icontains=categoria_nome)

    todas_categorias = CategoriaDoacao.objects.all()

    context = {
        'instituicoes': instituicoes,
        'cidade_filtro': cidade,
        'tipo_filtro': categoria_nome,
        'categorias': todas_categorias,
    }
    return render(request, "guiadoars/home.html", context)

from .models import Instituicao
from django.shortcuts import render

def lista_instituicoes(request):
    instituicoes = Instituicao.objects.all()
    return render(request, 'guiadoars/instituicoes.html', {
        'instituicoes': instituicoes
    })