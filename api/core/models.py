from django.db import models
from usuarios.models import Usuario  # Use sempre o modelo de usuarios

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
    
    # Paleta de cores principal
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
    
    # Cores de status e feedback
    cor_success = models.CharField(
        max_length=7, 
        default='#48c774',
        help_text='Cor de sucesso/confirmação em formato hexadecimal (ex: #48c774)'
    )
    
    cor_danger = models.CharField(
        max_length=7, 
        default='#f14668',
        help_text='Cor de erro/negação em formato hexadecimal (ex: #f14668)'
    )
    
    cor_warning = models.CharField(
        max_length=7, 
        default='#ffdd57',
        help_text='Cor de aviso em formato hexadecimal (ex: #ffdd57)'
    )
    
    cor_info = models.CharField(
        max_length=7, 
        default='#3298dc',
        help_text='Cor de informação em formato hexadecimal (ex: #3298dc)'
    )
    
    # Cores de interface
    cor_texto = models.CharField(
        max_length=7, 
        default='#363636',
        help_text='Cor principal do texto em formato hexadecimal (ex: #363636)'
    )
    
    cor_borda = models.CharField(
        max_length=7, 
        default='#dbdbdb',
        help_text='Cor das bordas em formato hexadecimal (ex: #dbdbdb)'
    )
    
    cor_sombra = models.CharField(
        max_length=7, 
        default='#000000',
        help_text='Cor das sombras em formato hexadecimal (ex: #000000)'
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


class Role(models.Model):
    """
    Modelo para definir roles/funções no sistema
    """
    name = models.CharField(
        max_length=50, 
        unique=True,
        help_text='Nome único do role (ex: admin, veterinario, recepcionista)'
    )
    display_name = models.CharField(
        max_length=100,
        help_text='Nome amigável para exibição (ex: Administrador, Veterinário)'
    )
    description = models.TextField(
        blank=True, 
        null=True,
        help_text='Descrição das responsabilidades deste role'
    )
    is_active = models.BooleanField(
        default=True,
        help_text='Se este role está ativo e pode ser atribuído'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Role'
        verbose_name_plural = 'Roles'
        ordering = ['name']

    def __str__(self):
        return self.display_name


class Permission(models.Model):
    """
    Modelo para definir permissões específicas no sistema
    """
    RESOURCE_CHOICES = [
        ('usuarios', 'Usuários'),
        ('agendamentos', 'Agendamentos'),
        ('animais', 'Animais'),
        ('servicos', 'Serviços'),
        ('configuracoes', 'Configurações'),
        ('relatorios', 'Relatórios'),
        ('brand', 'Marca/Branding'),
    ]
    
    ACTION_CHOICES = [
        ('create', 'Criar'),
        ('read', 'Visualizar'),
        ('update', 'Editar'),
        ('delete', 'Excluir'),
        ('list', 'Listar'),
        ('manage', 'Gerenciar'),
    ]

    resource = models.CharField(
        max_length=50, 
        choices=RESOURCE_CHOICES,
        help_text='Recurso sobre o qual a permissão se aplica'
    )
    action = models.CharField(
        max_length=20, 
        choices=ACTION_CHOICES,
        help_text='Ação permitida sobre o recurso'
    )
    description = models.CharField(
        max_length=200,
        help_text='Descrição clara da permissão'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Permissão'
        verbose_name_plural = 'Permissões'
        unique_together = ['resource', 'action']
        ordering = ['resource', 'action']

    def __str__(self):
        return f"{self.get_resource_display()} - {self.get_action_display()}"

    @property
    def codename(self):
        """Retorna um código único para a permissão"""
        return f"{self.action}_{self.resource}"


class RolePermission(models.Model):
    """
    Modelo de associação entre Roles e Permissions
    """
    role = models.ForeignKey(
        Role, 
        on_delete=models.CASCADE,
        related_name='permissions'
    )
    permission = models.ForeignKey(
        Permission, 
        on_delete=models.CASCADE,
        related_name='roles'
    )
    granted_at = models.DateTimeField(auto_now_add=True)
    granted_by = models.ForeignKey(
        Usuario, 
        on_delete=models.SET_NULL,
        null=True, 
        blank=True,
        help_text='Usuário que concedeu esta permissão'
    )

    class Meta:
        verbose_name = 'Permissão do Role'
        verbose_name_plural = 'Permissões dos Roles'
        unique_together = ['role', 'permission']

    def __str__(self):
        return f"{self.role.name} - {self.permission}"


class UserRole(models.Model):
    """
    Modelo de associação entre Usuários e Roles
    """
    user = models.ForeignKey(
        Usuario, 
        on_delete=models.CASCADE,
        related_name='user_roles'
    )
    role = models.ForeignKey(
        Role, 
        on_delete=models.CASCADE,
        related_name='user_assignments'
    )
    assigned_at = models.DateTimeField(auto_now_add=True)
    assigned_by = models.ForeignKey(
        Usuario, 
        on_delete=models.SET_NULL,
        null=True, 
        blank=True,
        related_name='role_assignments_made',
        help_text='Usuário que atribuiu este role'
    )
    is_active = models.BooleanField(
        default=True,
        help_text='Se esta atribuição está ativa'
    )

    class Meta:
        verbose_name = 'Role do Usuário'
        verbose_name_plural = 'Roles dos Usuários'
        unique_together = ['user', 'role']

    def __str__(self):
        return f"{self.user.nome} - {self.role.display_name}"