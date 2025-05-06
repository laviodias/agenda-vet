from django.db import models

class Servico(models.Model):
  nome = models.CharField(max_length=255, unique=True)
  descricao = models.TextField(blank=True, null=True)
  preco = models.DecimalField(max_digits=10, decimal_places=2)
  empresa = models.ForeignKey('core.Empresa', on_delete=models.CASCADE, related_name='servicos')

  def __str__(self):
    return self.nome