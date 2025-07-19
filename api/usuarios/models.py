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


class DisponibilidadeProfissional(models.Model):
    DIAS_SEMANA = (
        (0, 'Segunda-feira'),
        (1, 'Terça-feira'),
        (2, 'Quarta-feira'),
        (3, 'Quinta-feira'),
        (4, 'Sexta-feira'),
        (5, 'Sábado'),
        (6, 'Domingo'),
    )
    
    profissional = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='disponibilidades')
    dia_semana = models.IntegerField(choices=DIAS_SEMANA)
    hora_inicio = models.TimeField()
    hora_fim = models.TimeField()
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['profissional', 'dia_semana']
        ordering = ['profissional', 'dia_semana']
    
    def __str__(self):
        return f"{self.profissional.nome} - {self.get_dia_semana_display()} ({self.hora_inicio} às {self.hora_fim})"
    
    def clean(self):
        from django.core.exceptions import ValidationError
        if self.hora_inicio >= self.hora_fim:
            raise ValidationError('Hora de início deve ser menor que hora de fim')
    
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)