from rest_framework import serializers
from .models import Empresa, ConfiguracaoBrand, Role, Permission, RolePermission, UserRole
from usuarios.models import Usuario


class EmpresaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empresa
        fields = '__all__'


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
    
    def validate_cor_success(self, value):
        if not value.startswith('#') or len(value) != 7:
            raise serializers.ValidationError('Cor deve estar no formato hexadecimal (#RRGGBB)')
        return value
    
    def validate_cor_danger(self, value):
        if not value.startswith('#') or len(value) != 7:
            raise serializers.ValidationError('Cor deve estar no formato hexadecimal (#RRGGBB)')
        return value
    
    def validate_cor_warning(self, value):
        if not value.startswith('#') or len(value) != 7:
            raise serializers.ValidationError('Cor deve estar no formato hexadecimal (#RRGGBB)')
        return value
    
    def validate_cor_info(self, value):
        if not value.startswith('#') or len(value) != 7:
            raise serializers.ValidationError('Cor deve estar no formato hexadecimal (#RRGGBB)')
        return value
    
    def validate_cor_texto(self, value):
        if not value.startswith('#') or len(value) != 7:
            raise serializers.ValidationError('Cor deve estar no formato hexadecimal (#RRGGBB)')
        return value
    
    def validate_cor_borda(self, value):
        if not value.startswith('#') or len(value) != 7:
            raise serializers.ValidationError('Cor deve estar no formato hexadecimal (#RRGGBB)')
        return value
    
    def validate_cor_sombra(self, value):
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
        fields = ['id', 'resource', 'action', 'description', 'resource_display', 'action_display', 'codename']


class RolePermissionSerializer(serializers.ModelSerializer):
    permission = PermissionSerializer(read_only=True)
    
    class Meta:
        model = RolePermission
        fields = ['id', 'permission', 'granted_at', 'granted_by']


class RoleSerializer(serializers.ModelSerializer):
    permissions = RolePermissionSerializer(many=True, read_only=True)
    permissions_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Role
        fields = ['id', 'name', 'display_name', 'description', 'is_active', 'created_at', 'updated_at', 'permissions', 'permissions_count']
    
    def get_permissions_count(self, obj):
        return obj.permissions.count()


class UserRoleSerializer(serializers.ModelSerializer):
    role = RoleSerializer(read_only=True)
    user_name = serializers.CharField(source='user.nome', read_only=True)
    user_email = serializers.CharField(source='user.email', read_only=True)
    
    class Meta:
        model = UserRole
        fields = ['id', 'role', 'user_name', 'user_email', 'assigned_at', 'assigned_by', 'is_active']


class AssignRoleSerializer(serializers.Serializer):
    roles = serializers.ListField(child=serializers.IntegerField())


class UserPermissionsSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    permissions = serializers.ListField(child=serializers.CharField())


# Serializers para as novas views de roles
class CreateRoleSerializer(serializers.ModelSerializer):
    permissions = serializers.ListField(child=serializers.IntegerField(), required=False)
    
    class Meta:
        model = Role
        fields = ['name', 'display_name', 'description', 'permissions']


class UpdateRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['name', 'display_name', 'description']


class AssignPermissionsSerializer(serializers.Serializer):
    permissions = serializers.ListField(child=serializers.IntegerField())


class AssignUserRolesSerializer(serializers.Serializer):
    roles = serializers.ListField(child=serializers.IntegerField())


class RoleStatsSerializer(serializers.Serializer):
    rolesCount = serializers.IntegerField()
    permissionsCount = serializers.IntegerField()
    usersCount = serializers.IntegerField()
    assignmentsCount = serializers.IntegerField() 