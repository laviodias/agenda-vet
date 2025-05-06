from django.db import models
from usuarios.models import Usuario

class Empresa(models.Model):
  nome = models.CharField(max_length=255, unique=True)
  cnpj = models.CharField(max_length=18, unique=True, blank=True, null=True)
  endereco = models.TextField(blank=True, null=True)
  telefone = models.CharField(max_length=20, blank=True, null=True)
  admins = models.ManyToManyField(Usuario, related_name='empresas_administradas')

  def __str__(self):
    return self.nome