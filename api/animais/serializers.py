from rest_framework import serializers
from .models import Animal

class AnimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Animal
        fields = ['id', 'dono', 'empresa', 'nome', 'especie', 'raca', 'data_nascimento']
        read_only_fields = ['id'] 