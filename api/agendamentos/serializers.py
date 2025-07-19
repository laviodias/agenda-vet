from rest_framework import serializers
from .models import Agendamento

class AgendamentoSerializer(serializers.ModelSerializer):
    # Campos relacionados para o formato padronizado
    servico_nome = serializers.CharField(source='servico.nome', read_only=True)
    servico_preco = serializers.DecimalField(source='servico.preco', max_digits=10, decimal_places=2, read_only=True)
    pet_nome = serializers.CharField(source='animal.nome', read_only=True)
    pet_especie = serializers.CharField(source='animal.especie', read_only=True)
    cliente_nome = serializers.CharField(source='cliente.nome', read_only=True)
    
    class Meta:
        model = Agendamento
        fields = [
            'id', 'empresa', 'animal', 'servico', 'data_hora', 'observacoes', 'cliente', 'status',
            'servico_nome', 'servico_preco', 'pet_nome', 'pet_especie', 'cliente_nome'
        ]
        read_only_fields = ['id']
    
    def to_representation(self, instance):
        """
        Retorna os dados no formato padronizado
        """
        data = super().to_representation(instance)
        
        # Formato padronizado
        return {
            'id': data['id'],
            'data_hora': data['data_hora'],
            'servico': data['servico_nome'],
            'preco': float(data['servico_preco']),
            'pet_nome': data['pet_nome'],
            'pet_especie': data['pet_especie'],
            'cliente': data['cliente_nome'],
            'observacoes': data['observacoes'] or '',
            'status': data['status']
        } 