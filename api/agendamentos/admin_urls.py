from django.urls import path
from agendamentos import views
from usuarios import views as usuarios_views

urlpatterns = [
    # ===== URLs PARA ADMIN DE AGENDAMENTOS =====
    path('agendamentos/', views.get_agendamentos_admin, name='get_agendamentos_admin'),
    path('agendamentos/create/', views.create_agendamento_admin, name='create_agendamento_admin'),
    path('agendamentos/<int:agendamento_id>/', views.update_agendamento_admin, name='update_agendamento_admin'),
    path('agendamentos/<int:agendamento_id>/status/', views.update_agendamento_status_admin, name='update_agendamento_status_admin'),
    path('agendamentos/<int:agendamento_id>/delete/', views.delete_agendamento_admin, name='delete_agendamento_admin'),
    path('agendamentos/stats/', views.get_agendamento_stats_admin, name='get_agendamento_stats_admin'),
    
    # ===== URLs PARA ADMIN DE SERVIÇOS =====
    path('servicos/', views.get_servicos_admin, name='get_servicos_admin'),
] 