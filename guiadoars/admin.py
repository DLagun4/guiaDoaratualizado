from django.contrib import admin
from .models import Instituicao, CategoriaDoacao

@admin.register(Instituicao)
class InstituicaoAdmin(admin.ModelAdmin):
    list_display = [
        'nome',
        'cidade',
        'estado',
        'tipo_instituicao',
        'telefone',
        'ativa',
        'data_cadastro'
    ]
    list_display_links = ['nome']
    list_filter = [
        'ativa',
        'tipo_instituicao',
        'cidade',
        'estado',
        'data_cadastro'
    ]
    search_fields = [
        'nome',
        'cidade',
        'endereco',
        'descricao',
        # Não use 'tipos_doacao' pois foi substituído por 'categorias_doacao'
    ]
    filter_horizontal = ['categorias_doacao']   # Campo ManyToMany
    fieldsets = [
        (
            'Informações Básicas',
            {
                'fields': ['nome', 'descricao', 'tipo_instituicao', 'ativa']
            }
        ),
        (
            'Endereço',
            {
                'fields': ['endereco', 'cidade', 'estado', 'cep']
            }
        ),
        (
            'Contato',
            {
                'fields': ['telefone', 'email', 'site']
            }
        ),
        (
            'Doações',
            {
                'fields': ['categorias_doacao'],   # substituído
                'description': 'Selecione uma ou mais categorias de doação'
            }
        ),
        (
            'Geolocalização (opcional)',
            {
                'fields': ['latitude', 'longitude'],
                'classes': ['collapse']
            }
        ),
    ]
    readonly_fields = ['data_cadastro']
    list_per_page = 25

# Registra o modelo CategoriaDoacao
admin.site.register(CategoriaDoacao)