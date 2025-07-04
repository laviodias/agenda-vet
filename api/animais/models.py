from django.db import models
from django.conf import settings

class Animal(models.Model):
  dono = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='animais')
  empresa = models.ForeignKey('core.Empresa', on_delete=models.CASCADE, related_name='animais')
  nome = models.CharField(max_length=100)
  especie = models.CharField(max_length=100)
  raca = models.CharField(max_length=100, blank=True, null=True)
  data_nascimento = models.DateField(blank=True, null=True)
  peso = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, help_text='Peso em kg')
  observacoes = models.TextField(blank=True, null=True)

  def __str__(self):
    return self.nome