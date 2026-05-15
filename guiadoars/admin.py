from django.contrib import admin
from .models import Instituicao, CategoriaDoacao, HorarioFuncionamento, SugestaoInstituicao

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


@admin.register(SugestaoInstituicao)
class SugestaoInstituicaoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'cidade', 'estado', 'tipo_instituicao', 'status', 'data_envio']
    list_filter = ['status', 'tipo_instituicao', 'estado']
    search_fields = ['nome', 'cidade', 'email']
    readonly_fields = ['data_envio']
    list_per_page = 25
    actions = ['aprovar_sugestoes', 'rejeitar_sugestoes']

    fieldsets = [
        ('Informações da Sugestão', {
            'fields': ['nome', 'descricao', 'tipo_instituicao', 'categorias_doacao_texto']
        }),
        ('Endereço', {
            'fields': ['endereco', 'cidade', 'estado', 'cep']
        }),
        ('Contato', {
            'fields': ['telefone', 'email', 'site']
        }),
        ('Moderação', {
            'fields': ['status', 'observacao_admin', 'data_envio']
        }),
    ]

    @admin.action(description='Aprovar sugestões selecionadas')
    def aprovar_sugestoes(self, request, queryset):
        atualizadas = queryset.update(status='aprovado')
        self.message_user(request, f'{atualizadas} sugestão(ões) aprovada(s).')

    @admin.action(description='Rejeitar sugestões selecionadas')
    def rejeitar_sugestoes(self, request, queryset):
        atualizadas = queryset.update(status='rejeitado')
        self.message_user(request, f'{atualizadas} sugestão(ões) rejeitada(s).')