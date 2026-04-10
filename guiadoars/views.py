"""Busca dados no banco
Guarda na variável instituicoes
Envia para o template home.html"""

from django.shortcuts import render
from .models import Instituicao, CategoriaDoacao


def index(request):
    """Página principal com busca por cidade, múltiplos tipos de doação e tipo de instituição"""

    cidade = request.GET.get('cidade', '').strip()
    tipos_selecionados = request.GET.getlist('tipo')   # lista de nomes das categorias
    tipo_inst = request.GET.get('tipo_inst', '')

    # Base: instituições ativas
    instituicoes = Instituicao.objects.filter(ativa=True)

    if cidade:
        instituicoes = instituicoes.filter(cidade__icontains=cidade)

    if tipos_selecionados:
        instituicoes = instituicoes.filter(categorias_doacao__nome__in=tipos_selecionados).distinct()

    if tipo_inst:
        instituicoes = instituicoes.filter(tipo_instituicao=tipo_inst)

    todas_categorias = CategoriaDoacao.objects.all()
    tipos_choices = Instituicao.TIPO_INSTITUICAO_CHOICES

    context = {
        'instituicoes': instituicoes,
        'cidade_filtro': cidade,
        'tipos_selecionados': tipos_selecionados,
        'tipo_inst_filtro': tipo_inst,
        'categorias': todas_categorias,
        'tipos_instituicao_choices': tipos_choices,
    }
    return render(request, "guiadoars/home.html", context)


from .models import Instituicao
from django.shortcuts import render

def lista_instituicoes(request):
    instituicoes = Instituicao.objects.all()
    return render(request, 'guiadoars/instituicoes.html', {
        'instituicoes': instituicoes
    })