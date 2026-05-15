from django.db import models
from django.utils import timezone
from .utils import geocode_endereco

class CategoriaDoacao(models.Model):
    nome = models.CharField(max_length=100, unique=True, verbose_name="Nome da categoria")
    descricao = models.TextField(blank=True, verbose_name="Descrição")
    personalizada = models.BooleanField(default=False, verbose_name="Categoria personalizada?")

    class Meta:
        verbose_name = "Categoria de Doação"
        verbose_name_plural = "Categorias de Doação"
        ordering = ['nome']

    def __str__(self):
        return self.nome

class HorarioFuncionamento(models.Model):
    DIAS_SEMANA = [
        (0, 'Segunda-feira'),
        (1, 'Terça-feira'),
        (2, 'Quarta-feira'),
        (3, 'Quinta-feira'),
        (4, 'Sexta-feira'),
        (5, 'Sábado'),
        (6, 'Domingo'),
    ]

    instituicao = models.ForeignKey('Instituicao', on_delete=models.CASCADE, related_name='horarios')
    dia_semana = models.IntegerField(choices=DIAS_SEMANA, verbose_name="Dia da semana")
    abertura = models.TimeField(verbose_name="Abre às")
    fechamento = models.TimeField(verbose_name="Fecha às")
    intervalo_inicio = models.TimeField(blank=True, null=True, verbose_name="Intervalo (início)")
    intervalo_fim = models.TimeField(blank=True, null=True, verbose_name="Intervalo (fim)")

    class Meta:
        verbose_name = "Horário de funcionamento"
        verbose_name_plural = "Horários de funcionamento"
        ordering = ['instituicao', 'dia_semana']

    def __str__(self):
        return f"{self.get_dia_semana_display()}: {self.abertura} - {self.fechamento}"

class Instituicao(models.Model):
    TIPO_INSTITUICAO_CHOICES = [
        ('abrigo', 'Abrigo'),
        ('ong', 'ONG'),
        ('igreja', 'Igreja'),
        ('escola', 'Escola'),
        ('hospital', 'Hospital'),
        ('outro', 'Outro'),
    ]

    # Campos básicos
    nome = models.CharField(max_length=200, verbose_name="Nome da Instituição")
    descricao = models.TextField(verbose_name="Descrição", blank=True)

    # Endereço
    endereco = models.CharField(max_length=255, verbose_name="Endereço", blank=True)
    cidade = models.CharField(max_length=100, verbose_name="Cidade")
    estado = models.CharField(max_length=2, verbose_name="Estado", blank=True)
    cep = models.CharField(max_length=9, verbose_name="CEP", blank=True, help_text="Formato: 00000-000")

    # Contato
    telefone = models.CharField(max_length=20, verbose_name="Telefone", blank=True)
    email = models.EmailField(verbose_name="E-mail", blank=True)
    site = models.URLField(verbose_name="Site", blank=True)

    # Relacionamento com categorias de doação
    categorias_doacao = models.ManyToManyField(
        CategoriaDoacao,
        blank=True,
        verbose_name="Categorias de doação aceitas",
        help_text="Selecione uma ou mais categorias"
    )

    # Classificação
    tipo_instituicao = models.CharField(
        max_length=20,
        choices=TIPO_INSTITUICAO_CHOICES,
        verbose_name="Tipo de Instituição",
        default='ong'
    )

    # Status e controle
    data_cadastro = models.DateTimeField(auto_now_add=True, verbose_name="Data de cadastro")
    ativa = models.BooleanField(default=True, verbose_name="Ativa?")

    # Geolocalização
    latitude = models.FloatField(blank=True, null=True, verbose_name="Latitude")
    longitude = models.FloatField(blank=True, null=True, verbose_name="Longitude")

    def save(self, *args, **kwargs):
        # Só geocodifica se não houver coordenadas
        if not self.latitude or not self.longitude:
            endereco_completo = f"{self.endereco}, {self.cidade}, {self.estado}, {self.cep}".strip(", ")
            if endereco_completo:
                lat, lng = geocode_endereco(endereco_completo)
                if lat and lng:
                    self.latitude = lat
                    self.longitude = lng
        super().save(*args, **kwargs)

    @property
    def aberto_agora(self):
        """Retorna True se aberto, False se fechado, None se sem horário cadastrado."""
        agora = timezone.localtime()
        dia_hoje = agora.weekday()  # 0=segunda, 6=domingo
        hora_atual = agora.time().replace(second=0, microsecond=0)

        horario = self.horarios.filter(dia_semana=dia_hoje).first()
        if not horario:
            return None

        if not (horario.abertura <= hora_atual <= horario.fechamento):
            return False

        if horario.intervalo_inicio and horario.intervalo_fim:
            if horario.intervalo_inicio <= hora_atual <= horario.intervalo_fim:
                return False

        return True

    class Meta:
        verbose_name = "Instituição"
        verbose_name_plural = "Instituições"
        ordering = ['nome']

    def __str__(self):
        return self.nome


class SugestaoInstituicao(models.Model):
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('aprovado', 'Aprovado'),
        ('rejeitado', 'Rejeitado'),
    ]

    nome = models.CharField(max_length=200, verbose_name="Nome da Instituição")
    descricao = models.TextField(blank=True, verbose_name="Descrição")
    endereco = models.CharField(max_length=255, blank=True, verbose_name="Endereço")
    cidade = models.CharField(max_length=100, verbose_name="Cidade")
    estado = models.CharField(max_length=2, verbose_name="Estado")
    cep = models.CharField(max_length=9, blank=True, verbose_name="CEP", help_text="Formato: 00000-000")
    telefone = models.CharField(max_length=20, blank=True, verbose_name="Telefone")
    email = models.EmailField(blank=True, verbose_name="E-mail")
    site = models.URLField(blank=True, verbose_name="Site")
    tipo_instituicao = models.CharField(
        max_length=20,
        choices=Instituicao.TIPO_INSTITUICAO_CHOICES,
        default='ong',
        verbose_name="Tipo de Instituição",
    )
    categorias_doacao_texto = models.TextField(
        blank=True,
        verbose_name="Tipos de doação aceitos",
        help_text="Ex: Roupas, Alimentos, Brinquedos",
    )

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente', verbose_name="Status")
    data_envio = models.DateTimeField(auto_now_add=True, verbose_name="Data de envio")
    observacao_admin = models.TextField(blank=True, verbose_name="Observação do administrador")

    class Meta:
        verbose_name = "Sugestão de Instituição"
        verbose_name_plural = "Sugestões de Instituições"
        ordering = ['-data_envio']

    def __str__(self):
        return f"{self.nome} ({self.get_status_display()})"