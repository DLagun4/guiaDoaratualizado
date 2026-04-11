from django.contrib import admin
from .models import Instituicao, CategoriaDoacao, HorarioFuncionamento

class HorarioInline(admin.TabularInline):
    model = HorarioFuncionamento
    extra = 1
    fields = ['dia_semana', 'abertura', 'fechamento', 'intervalo_inicio', 'intervalo_fim']

@admin.register(Instituicao)
class InstituicaoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'cidade', 'estado', 'tipo_instituicao', 'telefone', 'ativa', 'data_cadastro']
    list_filter = ['ativa', 'tipo_instituicao', 'cidade', 'estado']
    search_fields = ['nome', 'cidade', 'endereco', 'descricao']
    filter_horizontal = ['categorias_doacao']
    inlines = [HorarioInline]
    readonly_fields = ['data_cadastro']
    list_per_page = 25

    fieldsets = [
        ('Informações Básicas', {
            'fields': ['nome', 'descricao', 'tipo_instituicao', 'ativa']
        }),
        ('Endereço', {
            'fields': ['endereco', 'cidade', 'estado', 'cep']
        }),
        ('Contato', {
            'fields': ['telefone', 'email', 'site']
        }),
        ('Doações', {
            'fields': ['categorias_doacao']
        }),
        ('Geolocalização ', {
            'fields': ['latitude', 'longitude'],
            'classes': ['collapse']
        }),
    ]

    class Media:
        js = ('guiadoars/js/admin_map.js',)

admin.site.register(CategoriaDoacao)