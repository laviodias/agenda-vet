from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
  TIPO_CHOICES = (
    ('cliente', 'Cliente'),
    ('admin', 'Administrador'),
  )
  tipo = models.CharField(max_length=10, choices=TIPO_CHOICES, default='cliente')
  nome = models.CharField(max_length=255, blank=True, null=True)
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