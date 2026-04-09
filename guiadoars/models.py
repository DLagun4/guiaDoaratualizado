from django.db import models

# Tabela Topic no banco de dados
class Topic(models.Model):
  """Um assunto sobre o qual o usuario esta aprendendo."""
  text = models.CharField(max_length=200) #No maximo 200 caracteres
  date_added = models.DateTimeField(auto_now_add=True) #Registrar a data e hora junto com o text

  def __str__(self): #Aparecer no Painel Administrativo
    """Devolve uma representacao em string do modelo."""
    return self.text
  
class Entry(models.Model):
  """Algo especifico aprendido sobre um assunto."""
  topic = models.ForeignKey(Topic, on_delete=models.CASCADE) #Para cada topico aqui, relaciona com um topico que existe
  text = models.TextField()
  date_added = models.DateTimeField(auto_now_add=True)

  class Meta:
    verbose_name_plural = 'entries' #Qnd o Django quiser usar o Entry no plural, muda a palavra p/ plural

  def __str__(self):
    """Devolve uma representacao em string do modelo."""
    return self.text[:50] + '...' #Mostra apenas os 50 primeiros caracteres
  
  from django.db import models

from django.db import models

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

class Instituicao(models.Model):
    # Choices para tipo de instituição
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
    estado = models.CharField(max_length=2, verbose_name="Estado", blank=True)  # Ex: SP, RJ
    cep = models.CharField(max_length=9, verbose_name="CEP", blank=True, help_text="Formato: 00000-000")
    
    # Contato
    telefone = models.CharField(max_length=20, verbose_name="Telefone", blank=True)
    email = models.EmailField(verbose_name="E-mail", blank=True)
    site = models.URLField(verbose_name="Site", blank=True)
    
    # Tipos de doação aceitos (pode ser um campo de texto simples ou ManyToMany futuramente)
    tipos_doacao = models.CharField(
        max_length=200, 
        verbose_name="Tipos de doação aceitos", 
        blank=True,
        help_text="Separe por vírgula. Ex: roupas, alimentos, brinquedos"
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
    
    # Campos para geolocalização (futuro)
    latitude = models.FloatField(blank=True, null=True, verbose_name="Latitude")
    longitude = models.FloatField(blank=True, null=True, verbose_name="Longitude")

    class Meta:
        verbose_name = "Instituição"
        verbose_name_plural = "Instituições"
        ordering = ['nome']

    def __str__(self):
        return self.nome
  