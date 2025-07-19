from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import Usuario, DisponibilidadeProfissional
from animais.models import Animal


class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'username', 'email', 'nome', 'tipo', 'first_name', 'last_name', 'telefone', 'crmv', 'especialidade']
        read_only_fields = ['id']
        extra_kwargs = {
            'username': {'required': False},
            'email': {'required': True},
            'nome': {'required': True},
            'tipo': {'required': False},
        }

    def create(self, validated_data):
        # Sempre usar email como username
        validated_data['username'] = validated_data['email']
        
        # Definir tipo padrão se não fornecido
        if 'tipo' not in validated_data:
            validated_data['tipo'] = 'cliente'
        
        # Gerar first_name e last_name baseado no nome se não fornecidos
        if 'nome' in validated_data and not validated_data.get('first_name'):
            nome_parts = validated_data['nome'].split(' ', 1)
            validated_data['first_name'] = nome_parts[0]
            validated_data['last_name'] = nome_parts[1] if len(nome_parts) > 1 else ''
        
        return super().create(validated_data)


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
        
        # Criar pet usando empresa com ID 1 fixo
        from core.models import Empresa
        empresa = Empresa.objects.get(id=1)
        
        pet = Animal.objects.create(
            dono=user,
            empresa=empresa,
            **pet_data
        )
        
        return {
            'usuario': user,
            'pet': pet
        } 

class UsuarioCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['username', 'email', 'nome', 'tipo', 'telefone', 'endereco', 'crmv', 'especialidade', 'password']
        extra_kwargs = {
            'password': {'write_only': True},
            'username': {'required': False}
        }

    def create(self, validated_data):
        # Se username não foi fornecido, usar email
        if 'username' not in validated_data:
            validated_data['username'] = validated_data['email']
        
        # Definir tipo padrão se não fornecido
        if 'tipo' not in validated_data:
            validated_data['tipo'] = 'cliente'
        
        # Criar usuário com senha criptografada
        user = Usuario.objects.create_user(**validated_data)
        return user

class DisponibilidadeProfissionalSerializer(serializers.ModelSerializer):
    profissional_nome = serializers.CharField(source='profissional.nome', read_only=True)
    dia_semana_nome = serializers.CharField(source='get_dia_semana_display', read_only=True)
    
    class Meta:
        model = DisponibilidadeProfissional
        fields = ['id', 'profissional', 'profissional_nome', 'dia_semana', 'dia_semana_nome', 'hora_inicio', 'hora_fim', 'ativo', 'criado_em', 'atualizado_em']
        read_only_fields = ['id', 'criado_em', 'atualizado_em']

class DisponibilidadeProfissionalCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DisponibilidadeProfissional
        fields = ['profissional', 'dia_semana', 'hora_inicio', 'hora_fim', 'ativo'] 