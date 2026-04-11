from django.db import models
from .utils import geocode_endereco

# Tabela Topic no banco de dados
class Topic(models.Model):
    """Um assunto sobre o qual o usuario esta aprendendo."""
    text = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text

class Entry(models.Model):
    """Algo especifico aprendido sobre um assunto."""
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'entries'

    def __str__(self):
        return self.text[:50] + '...'

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

    class Meta:
        verbose_name = "Instituição"
        verbose_name_plural = "Instituições"
        ordering = ['nome']

    def __str__(self):
        return self.nome