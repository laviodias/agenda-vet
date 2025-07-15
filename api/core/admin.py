from django.contrib import admin
from usuarios.models import Usuario
from .models import Empresa, ConfiguracaoBrand, Role, Permission, RolePermission, UserRole

# Register your models here.

@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cnpj', 'telefone')
    search_fields = ('nome', 'cnpj')
    filter_horizontal = ('admins',)

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'tipo', 'is_active', 'date_joined')
    list_filter = ('tipo', 'is_active', 'date_joined')
    search_fields = ('nome', 'email', 'crmv')
    ordering = ('-date_joined',)
    
    fieldsets = (
        (None, {
            'fields': ('username', 'password')
        }),
        ('Informações Pessoais', {
            'fields': ('nome', 'email', 'telefone')
        }),
        ('Informações Profissionais', {
            'fields': ('tipo', 'crmv', 'especialidade')
        }),
        ('Permissões', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Datas Importantes', {
            'fields': ('last_login', 'date_joined')
        }),
    )
    readonly_fields = ('last_login', 'date_joined')

@admin.register(ConfiguracaoBrand)
class ConfiguracaoBrandAdmin(admin.ModelAdmin):
    list_display = ('nome_estabelecimento', 'ativo', 'criado_em')
    list_filter = ('ativo', 'criado_em')
    search_fields = ('nome_estabelecimento',)
    ordering = ('-criado_em',)


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('name', 'display_name', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'display_name')
    ordering = ('name',)
    
    fieldsets = (
        (None, {
            'fields': ('name', 'display_name', 'description', 'is_active')
        }),
        ('Auditoria', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ('resource', 'action', 'description', 'created_at')
    list_filter = ('resource', 'action', 'created_at')
    search_fields = ('resource', 'action', 'description')
    ordering = ('resource', 'action')
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # Editing existing permission
            return ['resource', 'action', 'created_at']
        return ['created_at']


class RolePermissionInline(admin.TabularInline):
    model = RolePermission
    extra = 0
    autocomplete_fields = ['permission']
    
    def get_readonly_fields(self, request, obj=None):
        return ['granted_at', 'granted_by']


@admin.register(RolePermission)
class RolePermissionAdmin(admin.ModelAdmin):
    list_display = ('role', 'permission', 'granted_at', 'granted_by')
    list_filter = ('granted_at', 'role', 'permission__resource', 'permission__action')
    search_fields = ('role__name', 'permission__resource', 'permission__action')
    ordering = ('-granted_at',)
    autocomplete_fields = ['role', 'permission', 'granted_by']
    
    def save_model(self, request, obj, form, change):
        if not obj.granted_by:
            obj.granted_by = request.user
        super().save_model(request, obj, form, change)


class UserRoleInline(admin.TabularInline):
    model = UserRole
    fk_name = 'user'  # Especificar qual ForeignKey usar
    extra = 0
    autocomplete_fields = ['role']
    
    def get_readonly_fields(self, request, obj=None):
        return ['assigned_at', 'assigned_by']


@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'is_active', 'assigned_at', 'assigned_by')
    list_filter = ('is_active', 'assigned_at', 'role', 'user__tipo')
    search_fields = ('user__nome', 'user__email', 'role__name')
    ordering = ('-assigned_at',)
    autocomplete_fields = ['user', 'role', 'assigned_by']
    
    def save_model(self, request, obj, form, change):
        if not obj.assigned_by:
            obj.assigned_by = request.user
        super().save_model(request, obj, form, change)


# Customize the Role admin to show permissions inline
class RoleAdminWithPermissions(RoleAdmin):
    inlines = [RolePermissionInline]


# Customize the Usuario admin to show roles inline  
class UsuarioAdminWithRoles(UsuarioAdmin):
    inlines = [UserRoleInline]


# Re-register with inlines
admin.site.unregister(Role)
admin.site.unregister(Usuario)
admin.site.register(Role, RoleAdminWithPermissions)
admin.site.register(Usuario, UsuarioAdminWithRoles)
