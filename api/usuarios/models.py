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
    return self.username

  def has_role(self, role_name):
    from core.models import UserRole  # Import local para evitar import circular
    return UserRole.objects.filter(user=self, role__name=role_name, is_active=True).exists()