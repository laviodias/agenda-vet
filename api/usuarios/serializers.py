from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import Usuario
from animais.models import Animal


class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'username', 'email', 'nome', 'tipo', 'first_name', 'last_name']
        read_only_fields = ['id']


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    senha = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        senha = attrs.get('senha')

        if email and senha:
            # Tentar autenticar com email
            user = authenticate(username=email, password=senha)
            if not user:
                # Tentar autenticar com username
                user = authenticate(username=email, password=senha)
            
            if user:
                attrs['user'] = user
                return attrs
            else:
                raise serializers.ValidationError('Credenciais inválidas.')
        else:
            raise serializers.ValidationError('Email e senha são obrigatórios.')


class AnimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Animal
        fields = ['id', 'nome', 'especie', 'raca', 'data_nascimento']


class RegistroClienteSerializer(serializers.Serializer):
    # Dados do usuário
    nome = serializers.CharField(max_length=255)
    email = serializers.EmailField()
    telefone = serializers.CharField(max_length=20)
    senha = serializers.CharField(write_only=True, min_length=6)
    
    # Dados do pet
    pet = AnimalSerializer()

    def create(self, validated_data):
        pet_data = validated_data.pop('pet')
        
        # Criar usuário
        user = Usuario.objects.create_user(
            username=validated_data['email'],
            email=validated_data['email'],
            password=validated_data['senha'],
            nome=validated_data['nome'],
            tipo='cliente'
        )
        
        # Criar pet (assumindo que temos uma empresa padrão)
        from core.models import Empresa
        empresa_padrao, created = Empresa.objects.get_or_create(
            nome='Clínica Veterinária Padrão',
            defaults={
                'cnpj': '00.000.000/0001-00',
                'endereco': 'Endereço padrão',
                'telefone': '(11) 99999-9999'
            }
        )
        
        pet = Animal.objects.create(
            dono=user,
            empresa=empresa_padrao,
            **pet_data
        )
        
        return {
            'usuario': user,
            'pet': pet
        } 