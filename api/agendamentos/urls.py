from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DisponibilidadeAgendaViewSet, AgendamentoViewSet
from . import views

router = DefaultRouter()
router.register(r'disponibilidades', DisponibilidadeAgendaViewSet)
router.register(r'agendamentos', AgendamentoViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('', views.listar_agendamentos_cliente, name='listar_agendamentos_cliente'),
    path('criar/', views.criar_agendamento, name='criar_agendamento'),
    path('horarios-disponiveis/', views.horarios_disponiveis, name='horarios_disponiveis'),
    path('<int:agendamento_id>/confirmar/', views.confirmar_agendamento, name='confirmar_agendamento'),
    path('<int:agendamento_id>/cancelar/', views.cancelar_agendamento, name='cancelar_agendamento'),
    
    # ===== URLs PARA ADMIN =====
    path('admin/agendamentos/', views.get_agendamentos_admin, name='get_agendamentos_admin'),
    path('admin/agendamentos/create/', views.create_agendamento_admin, name='create_agendamento_admin'),
    path('admin/agendamentos/<int:agendamento_id>/', views.update_agendamento_admin, name='update_agendamento_admin'),
    path('admin/agendamentos/<int:agendamento_id>/status/', views.update_agendamento_status_admin, name='update_agendamento_status_admin'),
    path('admin/agendamentos/<int:agendamento_id>/delete/', views.delete_agendamento_admin, name='delete_agendamento_admin'),
    path('admin/agendamentos/stats/', views.get_agendamento_stats_admin, name='get_agendamento_stats_admin'),
    path('admin/responsaveis/', views.get_responsaveis_admin, name='get_responsaveis_admin'),
    path('admin/servicos/', views.get_servicos_admin, name='get_servicos_admin'),
] 