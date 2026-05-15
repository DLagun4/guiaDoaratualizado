"""Busca dados no banco
Guarda na variável instituicoes
Envia para o template home.html"""

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Instituicao, CategoriaDoacao
from .forms import SugestaoInstituicaoForm


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

    # Instituições com coordenadas para o mapa (usa o mesmo filtro da busca)
    instituicoes_mapa = instituicoes.filter(
        latitude__isnull=False,
        longitude__isnull=False
    ).values('id', 'nome', 'latitude', 'longitude', 'cidade')

    context = {
        'instituicoes': instituicoes,
        'cidade_filtro': cidade,
        'tipos_selecionados': tipos_selecionados,
        'tipo_inst_filtro': tipo_inst,
        'categorias': todas_categorias,
        'tipos_instituicao_choices': tipos_choices,
        'instituicoes_mapa': list(instituicoes_mapa),  # lista de dicionários
    }
    return render(request, "guiadoars/home.html", context)


def lista_instituicoes(request):
    instituicoes = Instituicao.objects.filter(ativa=True)
    return render(request, 'guiadoars/instituicoes.html', {
        'instituicoes': instituicoes
    })


def instituicao_detail(request, pk):
    instituicao = get_object_or_404(Instituicao, pk=pk, ativa=True)
    return render(request, 'guiadoars/instituicao_detail.html', {
        'instituicao': instituicao
    })


def sugerir_instituicao(request):
    if request.method == 'POST':
        form = SugestaoInstituicaoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Sugestão enviada com sucesso! Nossa equipe irá analisar em breve.')
            return redirect('sugerir_instituicao')
    else:
        form = SugestaoInstituicaoForm()
    return render(request, 'guiadoars/sugerir_instituicao.html', {'form': form})