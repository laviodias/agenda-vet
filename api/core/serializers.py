from rest_framework import serializers
from .models import Empresa, Usuario, ConfiguracaoBrand


class EmpresaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empresa
        fields = ['id', 'nome', 'cnpj', 'endereco', 'telefone', 'admins']
        read_only_fields = ['id']


class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'nome', 'email', 'telefone', 'tipo_usuario', 'crmv', 'especialidade', 'is_active']
        read_only_fields = ['id']


class ConfiguracaoBrandSerializer(serializers.ModelSerializer):
    logo_url = serializers.SerializerMethodField()
    
    class Meta:
        model = ConfiguracaoBrand
        fields = [
            'id', 'nome_estabelecimento', 'logo', 'logo_url',
            'cor_primaria', 'cor_secundaria', 'cor_accent', 'cor_background',
            'endereco', 'telefone', 'email', 'website',
            'criado_em', 'atualizado_em', 'ativo'
        ]
        read_only_fields = ['id', 'criado_em', 'atualizado_em']
    
    def get_logo_url(self, obj):
        """
        Retorna a URL completa do logo se existir
        """
        if obj.logo:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.logo.url)
            return obj.logo.url
        return None
    
    def validate_cor_primaria(self, value):
        """
        Validar formato hexadecimal da cor primária
        """
        if value and (not value.startswith('#') or len(value) != 7):
            raise serializers.ValidationError("Cor deve estar no formato #RRGGBB")
        if value:
            try:
                int(value[1:], 16)
            except ValueError:
                raise serializers.ValidationError("Formato de cor hexadecimal inválido")
        return value
    
    def validate_cor_secundaria(self, value):
        """
        Validar formato hexadecimal da cor secundária
        """
        if value and (not value.startswith('#') or len(value) != 7):
            raise serializers.ValidationError("Cor deve estar no formato #RRGGBB")
        if value:
            try:
                int(value[1:], 16)
            except ValueError:
                raise serializers.ValidationError("Formato de cor hexadecimal inválido")
        return value
    
    def validate_cor_accent(self, value):
        """
        Validar formato hexadecimal da cor de destaque
        """
        if value and (not value.startswith('#') or len(value) != 7):
            raise serializers.ValidationError("Cor deve estar no formato #RRGGBB")
        if value:
            try:
                int(value[1:], 16)
            except ValueError:
                raise serializers.ValidationError("Formato de cor hexadecimal inválido")
        return value
    
    def validate_cor_background(self, value):
        """
        Validar formato hexadecimal da cor de fundo
        """
        if value and (not value.startswith('#') or len(value) != 7):
            raise serializers.ValidationError("Cor deve estar no formato #RRGGBB")
        if value:
            try:
                int(value[1:], 16)
            except ValueError:
                raise serializers.ValidationError("Formato de cor hexadecimal inválido")
        return value 