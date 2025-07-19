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
    
    # URLs para gestão de clientes
    path('admin/clientes/', views.get_clientes, name='get_clientes'),  # GET - listar clientes
    path('admin/clientes/create/', views.create_cliente, name='create_cliente'),  # POST - criar cliente
    path('admin/clientes/<int:cliente_id>/', views.update_cliente, name='update_cliente'),  # PUT - atualizar cliente
    path('admin/clientes/<int:cliente_id>/toggle/', views.toggle_cliente_status, name='toggle_cliente_status'),  # PATCH - toggle status
    path('admin/clientes/stats/', views.get_cliente_stats, name='get_cliente_stats'),  # GET - estatísticas de clientes
    path('admin/clientes/<int:cliente_id>/detail/', views.get_cliente_detail, name='get_cliente_detail'),  # GET - detalhes do cliente
    path('admin/clientes/<int:cliente_id>/animais/', views.get_cliente_animais, name='get_cliente_animais'),  # GET - animais do cliente
    path('admin/clientes/<int:cliente_id>/agendamentos/', views.get_cliente_agendamentos, name='get_cliente_agendamentos'),  # GET - agendamentos do cliente
    
    # URLs para gestão de animais
    path('admin/animais/', views.get_animais, name='get_animais'),  # GET - listar animais
    path('admin/animais/create/', views.create_animal, name='create_animal'),  # POST - criar animal
    path('admin/animais/<int:animal_id>/', views.update_animal, name='update_animal'),  # PUT - atualizar animal
    path('admin/animais/stats/', views.get_animal_stats, name='get_animal_stats'),  # GET - estatísticas de animais
    path('admin/animais/<int:animal_id>/detail/', views.get_animal_detail, name='get_animal_detail'),  # GET - detalhes do animal
    path('admin/animais/<int:animal_id>/agendamentos/', views.get_animal_agendamentos, name='get_animal_agendamentos'),  # GET - agendamentos do animal
    
    # URLs para gestão de serviços
    path('admin/servicos/', views.get_servicos_admin, name='get_servicos_admin'),  # GET - listar serviços
    path('admin/servicos/create/', views.create_servico_admin, name='create_servico_admin'),  # POST - criar serviço
    path('admin/servicos/<int:servico_id>/', views.update_servico_admin, name='update_servico_admin'),  # PUT - atualizar serviço
    path('admin/servicos/<int:servico_id>/delete/', views.delete_servico_admin, name='delete_servico_admin'),  # DELETE - excluir serviço
] 