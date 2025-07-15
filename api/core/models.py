from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    nome = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    telefone = models.CharField(max_length=20, blank=True, null=True)
    tipo_usuario = models.CharField(
        max_length=20,
        choices=[
            ('admin', 'Administrador'),
            ('veterinario', 'Veterinário'),
            ('cliente', 'Cliente'),
        ],
        default='cliente'
    )
    crmv = models.CharField(max_length=20, blank=True, null=True)
    especialidade = models.CharField(max_length=100, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nome']

    def __str__(self):
        return self.nome


class Empresa(models.Model):
    nome = models.CharField(max_length=255, unique=True)
    cnpj = models.CharField(max_length=18, unique=True, blank=True, null=True)
    endereco = models.TextField(blank=True, null=True)
    telefone = models.CharField(max_length=20, blank=True, null=True)
    admins = models.ManyToManyField(Usuario, related_name='empresas_administradas')

    def __str__(self):
        return self.nome


class ConfiguracaoBrand(models.Model):
    """
    Modelo para armazenar configurações de marca/branding do estabelecimento
    """
    nome_estabelecimento = models.CharField(
        max_length=255, 
        default='AgendaVet',
        help_text='Nome do estabelecimento veterinário'
    )
    
    logo = models.ImageField(
        upload_to='brand/logos/', 
        blank=True, 
        null=True,
        help_text='Logo do estabelecimento (formato PNG ou JPG recomendado)'
    )
    
    # Paleta de cores
    cor_primaria = models.CharField(
        max_length=7, 
        default='#00d1b2',
        help_text='Cor primária em formato hexadecimal (ex: #00d1b2)'
    )
    
    cor_secundaria = models.CharField(
        max_length=7, 
        default='#363636',
        help_text='Cor secundária em formato hexadecimal (ex: #363636)'
    )
    
    cor_accent = models.CharField(
        max_length=7, 
        default='#3273dc',
        help_text='Cor de destaque em formato hexadecimal (ex: #3273dc)'
    )
    
    cor_background = models.CharField(
        max_length=7, 
        default='#f5f5f5',
        help_text='Cor de fundo em formato hexadecimal (ex: #f5f5f5)'
    )
    
    # Informações adicionais
    endereco = models.TextField(blank=True, null=True, help_text='Endereço completo do estabelecimento')
    telefone = models.CharField(max_length=20, blank=True, null=True, help_text='Telefone principal')
    email = models.EmailField(blank=True, null=True, help_text='E-mail de contato')
    website = models.URLField(blank=True, null=True, help_text='Website do estabelecimento')
    
    # Metadados
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    ativo = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'Configuração de Marca'
        verbose_name_plural = 'Configurações de Marca'
        
    def __str__(self):
        return f'Brand Config - {self.nome_estabelecimento}'
    
    def save(self, *args, **kwargs):
        # Garantir que apenas uma configuração esteja ativa
        if self.ativo:
            ConfiguracaoBrand.objects.filter(ativo=True).update(ativo=False)
        super().save(*args, **kwargs)
    
    @classmethod
    def get_configuracao_ativa(cls):
        """
        Retorna a configuração de marca ativa ou cria uma padrão
        """
        try:
            return cls.objects.filter(ativo=True).first()
        except cls.DoesNotExist:
            return cls.objects.create(
                nome_estabelecimento='AgendaVet',
                ativo=True
            )