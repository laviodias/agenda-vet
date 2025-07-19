from rest_framework import serializers
from .models import Agendamento

class AgendamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agendamento
        fields = ['id', 'empresa', 'animal', 'servico', 'data_hora', 'observacoes', 'cliente', 'status']
        read_only_fields = ['id'] 