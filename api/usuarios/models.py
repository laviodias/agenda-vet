from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
  TIPO_CHOICES = (
    ('cliente', 'Cliente'),
    ('admin', 'Administrador'),
    ('profissional', 'Profissional'),
  )
  tipo = models.CharField(max_length=15, choices=TIPO_CHOICES, default='cliente')
  nome = models.CharField(max_length=255, blank=True, null=True)
  telefone = models.CharField(max_length=20, blank=True, null=True)
  endereco = models.TextField(blank=True, null=True)
  crmv = models.CharField(max_length=20, blank=True, null=True)  # Para profissionais
  especialidade = models.CharField(max_length=100, blank=True, null=True)  # Para profissionais
  groups = models.ManyToManyField(
    'auth.Group',
    verbose_name='groups',
    blank=True,
    help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
    related_name="usuarios_set",
    related_query_name="usuario",
  )
  user_permissions = models.ManyToManyField(
    'auth.Permission',
    verbose_name='user permissions',
    blank=True,
    help_text='Specific permissions for this user.',
    related_name="usuarios_permissions_set",
    related_query_name="usuario_permission",
  )

  def __str__(self):
    return self.nome or self.email or self.username

  def has_role(self, role_name):
    from core.models import UserRole  # Import local para evitar import circular
    return UserRole.objects.filter(user=self, role__name=role_name, is_active=True).exists()

  def has_permission(self, resource, action):
    """
    Verificar se o usuário tem uma permissão específica
    """
    from core.models import UserRole, RolePermission  # Import local para evitar import circular
    
    # Buscar roles ativos do usuário
    user_roles = UserRole.objects.filter(user=self, is_active=True).values_list('role_id', flat=True)
    
    # Buscar permissões dos roles do usuário
    permissions = RolePermission.objects.filter(
        role_id__in=user_roles,
        permission__resource=resource,
        permission__action=action
    )
    
    return permissions.exists()

  def get_permissions(self):
    """
    Retornar todas as permissões do usuário
    """
    from core.models import UserRole, RolePermission  # Import local para evitar import circular
    
    # Buscar roles ativos do usuário
    user_roles = UserRole.objects.filter(user=self, is_active=True).values_list('role_id', flat=True)
    
    # Buscar permissões dos roles do usuário
    permissions = RolePermission.objects.filter(role_id__in=user_roles).select_related('permission')
    
    return [rp.permission for rp in permissions]

  def get_roles(self):
    """
    Retornar todos os roles ativos do usuário
    """
    from core.models import UserRole  # Import local para evitar import circular
    return UserRole.objects.filter(user=self, is_active=True).select_related('role')