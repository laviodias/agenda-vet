from django.urls import path
from . import views
from usuarios import views as usuarios_views

urlpatterns = [
    # ===== URLs PARA ADMIN DE AGENDAMENTOS =====
    path('agendamentos/', views.get_agendamentos_admin, name='get_agendamentos_admin'),
    path('agendamentos/create/', views.create_agendamento_admin, name='create_agendamento_admin'),
    path('agendamentos/<int:agendamento_id>/', views.update_agendamento_admin, name='update_agendamento_admin'),
    path('agendamentos/<int:agendamento_id>/status/', views.update_agendamento_status_admin, name='update_agendamento_status_admin'),
    path('agendamentos/<int:agendamento_id>/delete/', views.delete_agendamento_admin, name='delete_agendamento_admin'),
    path('agendamentos/stats/', views.get_agendamento_stats_admin, name='get_agendamento_stats_admin'),
    path('responsaveis/', views.get_responsaveis_admin, name='get_responsaveis_admin'),
    path('servicos/', views.get_servicos_admin, name='get_servicos_admin'),
    
    # ===== URLs PARA ADMIN DE HORÁRIOS DISPONÍVEIS =====
    path('horarios-disponiveis/', views.get_horarios_disponiveis_admin, name='get_horarios_disponiveis_admin'),
    path('horarios-disponiveis/create/', views.create_horario_disponivel_admin, name='create_horario_disponivel_admin'),
    path('horarios-disponiveis/<int:disponibilidade_id>/delete/', views.delete_horario_disponivel_admin, name='delete_horario_disponivel_admin'),
    
    # ===== URLs PARA ADMIN DE DISPONIBILIDADE DOS PROFISSIONAIS =====
    path('profissionais/<int:profissional_id>/disponibilidades/', usuarios_views.get_disponibilidades_profissional, name='get_disponibilidades_profissional'),
    path('disponibilidades/create/', usuarios_views.create_disponibilidade_profissional, name='create_disponibilidade_profissional'),
    path('disponibilidades/<int:disponibilidade_id>/', usuarios_views.update_disponibilidade_profissional, name='update_disponibilidade_profissional'),
    path('disponibilidades/<int:disponibilidade_id>/delete/', usuarios_views.delete_disponibilidade_profissional, name='delete_disponibilidade_profissional'),
    path('profissionais/<int:profissional_id>/disponibilidades/bulk/', usuarios_views.bulk_update_disponibilidades, name='bulk_update_disponibilidades'),
    path('profissionais/disponiveis/', usuarios_views.get_profissionais_disponiveis, name='get_profissionais_disponiveis'),
] 