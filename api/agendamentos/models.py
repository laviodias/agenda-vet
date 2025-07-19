from django.db import models
from django.conf import settings
from core.models import Empresa
from servicos.models import Servico
from animais.models import Animal

class DisponibilidadeAgenda(models.Model):
  empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='disponibilidades')
  servico = models.ForeignKey(Servico, on_delete=models.CASCADE, related_name='disponibilidades')
  data = models.DateField()
  hora_inicio = models.TimeField()
  hora_fim = models.TimeField()
  responsavel = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='disponibilidades_responsavel')

  class Meta:
    unique_together = ('empresa', 'servico', 'data', 'hora_inicio')
    verbose_name = 'Disponibilidade na Agenda'
    verbose_name_plural = 'Disponibilidades na Agenda'

  def __str__(self):
    return f"{self.servico.nome} disponível em {self.data} das {self.hora_inicio} às {self.hora_fim}"
    
class Agendamento(models.Model):
  STATUS_CHOICES = [
    ('pendente', 'Pendente'),
    ('confirmado', 'Confirmado'),
    ('realizado', 'Realizado'),
    ('cancelado', 'Cancelado'),
  ]
  
  empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='agendamentos')
  animal = models.ForeignKey(Animal, on_delete=models.CASCADE, related_name='agendamentos')
  servico = models.ForeignKey(Servico, on_delete=models.CASCADE, related_name='agendamentos')
  data_hora = models.DateTimeField()
  observacoes = models.TextField(blank=True, null=True)
  cliente = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='agendamentos_cliente')
  responsavel = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='agendamentos_responsavel')
  status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente')

  def __str__(self):
    return f"Agendamento de {self.animal.nome} para {self.servico.nome} em {self.data_hora}"