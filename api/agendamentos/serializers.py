from rest_framework import serializers
from .models import DisponibilidadeAgenda, Agendamento
from servicos.models import Servico
from animais.models import Animal
from usuarios.models import Usuario

class DisponibilidadeAgendaSerializer(serializers.ModelSerializer):
    servico_nome = serializers.CharField(source='servico.nome', read_only=True)
    responsavel_nome = serializers.CharField(source='responsavel.nome', read_only=True)
    
    class Meta:
        model = DisponibilidadeAgenda
        fields = ['id', 'data', 'hora_inicio', 'hora_fim', 'servico_nome', 'responsavel_nome', 'servico', 'responsavel']

class AgendamentoSerializer(serializers.ModelSerializer):
    servico_nome = serializers.CharField(source='servico.nome', read_only=True)
    servico_preco = serializers.DecimalField(source='servico.preco', max_digits=10, decimal_places=2, read_only=True)
    animal_nome = serializers.CharField(source='animal.nome', read_only=True)
    animal_especie = serializers.CharField(source='animal.especie', read_only=True)
    cliente_nome = serializers.CharField(source='cliente.nome', read_only=True)
    responsavel_nome = serializers.CharField(source='responsavel.nome', read_only=True)
    
    class Meta:
        model = Agendamento
        fields = [
            'id', 'data_hora', 'observacoes', 'servico_nome', 'servico_preco',
            'animal_nome', 'animal_especie', 'cliente_nome', 'responsavel_nome',
            'servico', 'animal', 'cliente', 'responsavel'
        ]
        read_only_fields = ['id', 'cliente'] 