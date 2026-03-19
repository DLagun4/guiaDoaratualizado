from django.contrib import admin
from guiadoars.models import Topic, Entry

from django.contrib import admin
from .models import Instituicao

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

      # Campos que serão pesquisáveis
    search_fields = [
        'nome', 
        'cidade', 
        'endereco', 
        'descricao', 
        'tipos_doacao'
    ]
    
    # Organização dos campos no formulário de edição
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
                'fields': ['tipos_doacao'],
                'description': 'Tipos de doação aceitos (separados por vírgula)'
            }
        ),
        (
            'Geolocalização (opcional)',
            {
                'fields': ['latitude', 'longitude'],
                'classes': ['collapse']  # fica recolhido por padrão
            }
        ),
    ]
    
    # Campos somente leitura (opcional)
    readonly_fields = ['data_cadastro']
    
    # Paginação na listagem
    list_per_page = 25