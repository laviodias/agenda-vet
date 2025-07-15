from rest_framework import serializers
from .models import Empresa, Usuario, ConfiguracaoBrand, Role, Permission, RolePermission, UserRole


class EmpresaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empresa
        fields = '__all__'


class UsuarioSerializer(serializers.ModelSerializer):
    roles = serializers.SerializerMethodField()
    permissions = serializers.SerializerMethodField()
    
    class Meta:
        model = Usuario
        fields = ['id', 'nome', 'email', 'telefone', 'tipo_usuario', 'crmv', 'especialidade', 
                 'is_active', 'date_joined', 'roles', 'permissions']
        read_only_fields = ['date_joined']
    
    def get_roles(self, obj):
        """Retorna os roles ativos do usuário"""
        return [{'name': role.name, 'display_name': role.display_name} 
                for role in obj.get_roles()]
    
    def get_permissions(self, obj):
        """Retorna as permissões do usuário"""
        return [{'resource': perm.resource, 'action': perm.action, 'codename': perm.codename}
                for perm in obj.get_permissions()]


class ConfiguracaoBrandSerializer(serializers.ModelSerializer):
    logo_url = serializers.SerializerMethodField()
    
    class Meta:
        model = ConfiguracaoBrand
        fields = '__all__'
    
    def get_logo_url(self, obj):
        if obj.logo:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.logo.url)
            return obj.logo.url
        return None
    
    def validate_cor_primaria(self, value):
        if not value.startswith('#') or len(value) != 7:
            raise serializers.ValidationError('Cor deve estar no formato hexadecimal (#RRGGBB)')
        return value
    
    def validate_cor_secundaria(self, value):
        if not value.startswith('#') or len(value) != 7:
            raise serializers.ValidationError('Cor deve estar no formato hexadecimal (#RRGGBB)')
        return value
    
    def validate_cor_accent(self, value):
        if not value.startswith('#') or len(value) != 7:
            raise serializers.ValidationError('Cor deve estar no formato hexadecimal (#RRGGBB)')
        return value
    
    def validate_cor_background(self, value):
        if not value.startswith('#') or len(value) != 7:
            raise serializers.ValidationError('Cor deve estar no formato hexadecimal (#RRGGBB)')
        return value
    
    def validate_logo(self, value):
        if value:
            # Validar tamanho do arquivo (máx 2MB)
            if value.size > 2 * 1024 * 1024:
                raise serializers.ValidationError('O arquivo deve ter no máximo 2MB.')
            
            # Validar tipo do arquivo
            if not value.content_type.startswith('image/'):
                raise serializers.ValidationError('Apenas imagens são permitidas.')
        
        return value


class PermissionSerializer(serializers.ModelSerializer):
    resource_display = serializers.CharField(source='get_resource_display', read_only=True)
    action_display = serializers.CharField(source='get_action_display', read_only=True)
    
    class Meta:
        model = Permission
        fields = ['id', 'resource', 'action', 'description', 'resource_display', 
                 'action_display', 'codename', 'created_at']
        read_only_fields = ['created_at']


class RoleSerializer(serializers.ModelSerializer):
    permissions = PermissionSerializer(many=True, read_only=True)
    permissions_count = serializers.SerializerMethodField()
    users_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Role
        fields = ['id', 'name', 'display_name', 'description', 'is_active', 
                 'permissions', 'permissions_count', 'users_count', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']
    
    def get_permissions_count(self, obj):
        """Retorna o número de permissões do role"""
        return obj.permissions.count()
    
    def get_users_count(self, obj):
        """Retorna o número de usuários com este role"""
        return obj.user_assignments.filter(is_active=True).count()


class RolePermissionSerializer(serializers.ModelSerializer):
    role_name = serializers.CharField(source='role.name', read_only=True)
    role_display_name = serializers.CharField(source='role.display_name', read_only=True)
    permission_description = serializers.CharField(source='permission.description', read_only=True)
    granted_by_name = serializers.CharField(source='granted_by.nome', read_only=True)
    
    class Meta:
        model = RolePermission
        fields = ['id', 'role', 'permission', 'role_name', 'role_display_name',
                 'permission_description', 'granted_at', 'granted_by', 'granted_by_name']
        read_only_fields = ['granted_at', 'granted_by']
    
    def create(self, validated_data):
        # Automaticamente atribuir o usuário que está criando
        validated_data['granted_by'] = self.context['request'].user
        return super().create(validated_data)


class UserRoleSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.nome', read_only=True)
    user_email = serializers.CharField(source='user.email', read_only=True)
    role_name = serializers.CharField(source='role.name', read_only=True)
    role_display_name = serializers.CharField(source='role.display_name', read_only=True)
    assigned_by_name = serializers.CharField(source='assigned_by.nome', read_only=True)
    
    class Meta:
        model = UserRole
        fields = ['id', 'user', 'role', 'user_name', 'user_email', 'role_name', 
                 'role_display_name', 'is_active', 'assigned_at', 'assigned_by', 'assigned_by_name']
        read_only_fields = ['assigned_at', 'assigned_by']
    
    def create(self, validated_data):
        # Automaticamente atribuir o usuário que está criando
        validated_data['assigned_by'] = self.context['request'].user
        return super().create(validated_data)


class AssignRoleSerializer(serializers.Serializer):
    """
    Serializer para atribuir roles a usuários
    """
    user_id = serializers.IntegerField()
    role_id = serializers.IntegerField()
    
    def validate_user_id(self, value):
        try:
            Usuario.objects.get(id=value)
        except Usuario.DoesNotExist:
            raise serializers.ValidationError('Usuário não encontrado.')
        return value
    
    def validate_role_id(self, value):
        try:
            role = Role.objects.get(id=value)
            if not role.is_active:
                raise serializers.ValidationError('Role não está ativo.')
        except Role.DoesNotExist:
            raise serializers.ValidationError('Role não encontrado.')
        return value
    
    def validate(self, data):
        # Verificar se a atribuição já existe
        existing = UserRole.objects.filter(
            user_id=data['user_id'],
            role_id=data['role_id']
        ).first()
        
        if existing and existing.is_active:
            raise serializers.ValidationError('Usuário já possui este role.')
        
        return data


class UserPermissionsSerializer(serializers.Serializer):
    """
    Serializer para listar permissões de um usuário
    """
    user_id = serializers.IntegerField()
    
    def validate_user_id(self, value):
        try:
            Usuario.objects.get(id=value)
        except Usuario.DoesNotExist:
            raise serializers.ValidationError('Usuário não encontrado.')
        return value 