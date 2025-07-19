from django.urls import path
from . import views

urlpatterns = [
    # URLs existentes
    path('can-access-admin/', views.can_access_admin, name='can_access_admin'),
    path('brand/ativa/', views.get_brand_config, name='get_brand_config'),
    path('brand/', views.brand_config_list, name='brand_config_list'),
    path('brand/<int:pk>/', views.brand_config_detail, name='brand_config_detail'),
    path('brand/<int:pk>/ativar/', views.activate_brand_config, name='activate_brand_config'),
    
    # URLs para roles e permissões
    path('admin/roles/', views.get_roles, name='get_roles'),  # GET - listar roles
    path('admin/roles/create/', views.create_role, name='create_role'),  # POST - criar role
    path('admin/roles/<int:role_id>/', views.update_role, name='update_role'),  # PUT - atualizar role
    path('admin/roles/<int:role_id>/delete/', views.delete_role, name='delete_role'),  # DELETE - deletar role
    path('admin/roles/<int:role_id>/toggle/', views.toggle_role_status, name='toggle_role_status'),  # PATCH - toggle status
    path('admin/roles/<int:role_id>/permissions/', views.assign_permissions, name='assign_permissions'),  # POST - atribuir permissões
    path('admin/permissions/', views.get_permissions, name='get_permissions'),  # GET - listar permissões
    path('admin/users/', views.get_users, name='get_users'),  # GET - listar usuários
    path('admin/users/assign-roles/', views.assign_user_roles, name='assign_user_roles'),  # POST - atribuir roles
    path('admin/users/<int:user_id>/roles/', views.get_user_roles, name='get_user_roles'),  # GET - buscar roles do usuário
    path('admin/roles/stats/', views.get_role_stats, name='get_role_stats'),  # GET - estatísticas
] 