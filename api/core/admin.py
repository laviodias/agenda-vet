from django.contrib import admin
from django.contrib.admin import AdminSite
from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import path
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from django.db import transaction
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


# ===== PÁGINA CUSTOMIZADA DE GERENCIAMENTO DE ROLES =====

class RoleManagementAdmin(admin.ModelAdmin):
    """
    Admin customizado para gerenciamento avançado de roles e permissões
    """
    change_list_template = 'admin/role_management.html'
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('create-role/', self.admin_site.admin_view(self.create_role_view), name='create_role'),
            path('assign-permissions/', self.admin_site.admin_view(self.assign_permissions_view), name='assign_permissions'),
            path('assign-users/', self.admin_site.admin_view(self.assign_users_view), name='assign_users'),
            path('api/permissions/', self.admin_site.admin_view(self.get_permissions_api), name='get_permissions_api'),
            path('api/roles/', self.admin_site.admin_view(self.get_roles_api), name='get_roles_api'),
            path('api/users/', self.admin_site.admin_view(self.get_users_api), name='get_users_api'),
        ]
        return custom_urls + urls
    
    def create_role_view(self, request):
        """View para criar roles personalizados"""
        if request.method == 'POST':
            try:
                with transaction.atomic():
                    name = request.POST.get('name')
                    display_name = request.POST.get('display_name')
                    description = request.POST.get('description', '')
                    
                    # Criar o role
                    role = Role.objects.create(
                        name=name,
                        display_name=display_name,
                        description=description,
                        is_active=True
                    )
                    
                    # Atribuir permissões selecionadas
                    permissions = request.POST.getlist('permissions')
                    for perm_id in permissions:
                        try:
                            permission = Permission.objects.get(id=perm_id)
                            RolePermission.objects.create(
                                role=role,
                                permission=permission,
                                granted_by=request.user
                            )
                        except Permission.DoesNotExist:
                            continue
                    
                    messages.success(request, f'Role "{display_name}" criado com sucesso!')
                    return redirect('admin:core_role_changelist')
                    
            except Exception as e:
                messages.error(request, f'Erro ao criar role: {str(e)}')
        
        # Buscar todas as permissões disponíveis
        permissions = Permission.objects.all().order_by('resource', 'action')
        context = {
            'title': 'Criar Role Personalizado',
            'permissions': permissions,
            'opts': self.model._meta,
        }
        return render(request, 'admin/create_role.html', context)
    
    def assign_permissions_view(self, request):
        """View para atribuir permissões a roles existentes"""
        if request.method == 'POST':
            try:
                with transaction.atomic():
                    role_id = request.POST.get('role')
                    permissions = request.POST.getlist('permissions')
                    
                    role = Role.objects.get(id=role_id)
                    
                    # Limpar permissões existentes
                    RolePermission.objects.filter(role=role).delete()
                    
                    # Adicionar novas permissões
                    for perm_id in permissions:
                        try:
                            permission = Permission.objects.get(id=perm_id)
                            RolePermission.objects.create(
                                role=role,
                                permission=permission,
                                granted_by=request.user
                            )
                        except Permission.DoesNotExist:
                            continue
                    
                    messages.success(request, f'Permissões atualizadas para o role "{role.display_name}"!')
                    return redirect('admin:core_role_changelist')
                    
            except Exception as e:
                messages.error(request, f'Erro ao atualizar permissões: {str(e)}')
        
        # Buscar roles e permissões
        roles = Role.objects.filter(is_active=True).order_by('display_name')
        permissions = Permission.objects.all().order_by('resource', 'action')
        
        context = {
            'title': 'Atribuir Permissões',
            'roles': roles,
            'permissions': permissions,
            'opts': self.model._meta,
        }
        return render(request, 'admin/assign_permissions.html', context)
    
    def assign_users_view(self, request):
        """View para atribuir roles a usuários"""
        if request.method == 'POST':
            try:
                with transaction.atomic():
                    user_id = request.POST.get('user')
                    roles = request.POST.getlist('roles')
                    
                    user = Usuario.objects.get(id=user_id)
                    
                    # Limpar roles existentes
                    UserRole.objects.filter(user=user).delete()
                    
                    # Adicionar novos roles
                    for role_id in roles:
                        try:
                            role = Role.objects.get(id=role_id, is_active=True)
                            UserRole.objects.create(
                                user=user,
                                role=role,
                                assigned_by=request.user
                            )
                        except Role.DoesNotExist:
                            continue
                    
                    messages.success(request, f'Roles atribuídos ao usuário "{user.nome}"!')
                    return redirect('admin:core_role_changelist')
                    
            except Exception as e:
                messages.error(request, f'Erro ao atribuir roles: {str(e)}')
        
        # Buscar usuários e roles
        users = Usuario.objects.filter(is_active=True).order_by('nome')
        roles = Role.objects.filter(is_active=True).order_by('display_name')
        
        context = {
            'title': 'Atribuir Roles a Usuários',
            'users': users,
            'roles': roles,
            'opts': self.model._meta,
        }
        return render(request, 'admin/assign_users.html', context)
    
    @method_decorator(csrf_exempt)
    def get_permissions_api(self, request):
        """API para buscar permissões"""
        permissions = Permission.objects.all().order_by('resource', 'action')
        data = []
        for perm in permissions:
            data.append({
                'id': perm.id,
                'resource': perm.get_resource_display(),
                'action': perm.get_action_display(),
                'description': perm.description,
                'codename': perm.codename
            })
        return JsonResponse({'permissions': data})
    
    @method_decorator(csrf_exempt)
    def get_roles_api(self, request):
        """API para buscar roles"""
        roles = Role.objects.filter(is_active=True).order_by('display_name')
        data = []
        for role in roles:
            data.append({
                'id': role.id,
                'name': role.name,
                'display_name': role.display_name,
                'description': role.description
            })
        return JsonResponse({'roles': data})
    
    @method_decorator(csrf_exempt)
    def get_users_api(self, request):
        """API para buscar usuários"""
        users = Usuario.objects.filter(is_active=True).order_by('nome')
        data = []
        for user in users:
            data.append({
                'id': user.id,
                'nome': user.nome,
                'email': user.email,
                'tipo': user.get_tipo_display()
            })
        return JsonResponse({'users': data})
