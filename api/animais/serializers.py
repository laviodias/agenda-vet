from rest_framework import serializers
from .models import Animal

class AnimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Animal
        fields = ['id', 'nome', 'especie', 'raca', 'data_nascimento']
        read_only_fields = ['id', 'dono']

class AnimalDetailSerializer(serializers.ModelSerializer):
    dono_nome = serializers.CharField(source='dono.nome', read_only=True)
    
    class Meta:
        model = Animal
        fields = ['id', 'nome', 'especie', 'raca', 'data_nascimento', 'dono_nome', 'dono']
        read_only_fields = ['id'] 