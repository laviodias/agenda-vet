from rest_framework import serializers
from .models import DisponibilidadeAgenda, Agendamento

class DisponibilidadeAgendaSerializer(serializers.ModelSerializer):
    class Meta:
        model = DisponibilidadeAgenda
        fields = ['id', 'empresa', 'servico', 'data', 'hora_inicio', 'hora_fim', 'responsavel']
        read_only_fields = ['id']

class AgendamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agendamento
        fields = ['id', 'empresa', 'animal', 'servico', 'data_hora', 'observacoes', 'cliente', 'responsavel']
        read_only_fields = ['id'] 