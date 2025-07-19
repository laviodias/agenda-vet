from rest_framework import serializers
from .models import Servico

class ServicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Servico
        fields = ['id', 'nome', 'descricao', 'preco', 'duracao', 'empresa']
        extra_kwargs = {
            'empresa': {'required': False}
        }
    
    def create(self, validated_data):
        # Usar empresa com ID 1 fixo se não fornecida
        if 'empresa' not in validated_data:
            from core.models import Empresa
            validated_data['empresa'] = Empresa.objects.get(id=1)
        
        return super().create(validated_data) 