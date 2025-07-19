from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DisponibilidadeAgendaViewSet, AgendamentoViewSet
from . import views

router = DefaultRouter()
router.register(r'disponibilidades', DisponibilidadeAgendaViewSet)
router.register(r'agendamentos', AgendamentoViewSet)

urlpatterns = [
    # ===== ROTAS PRINCIPAIS =====
    path('listar/', views.listar_todos_agendamentos, name='listar_todos_agendamentos'),
    path('listar-cliente/', views.listar_agendamentos_cliente, name='listar_agendamentos_cliente'),
    path('criar/', views.criar_agendamento, name='criar_agendamento'),
    path('horarios-disponiveis/', views.horarios_disponiveis, name='horarios_disponiveis'),
    path('<int:agendamento_id>/confirmar/', views.confirmar_agendamento, name='confirmar_agendamento'),
    path('<int:agendamento_id>/cancelar/', views.cancelar_agendamento, name='cancelar_agendamento'),
    
    # ===== URLs PARA DASHBOARD =====
    path('dashboard/', views.dashboard_stats, name='dashboard_stats'),
    path('recentes/', views.agendamentos_recentes, name='agendamentos_recentes'),
    
    # ===== ROUTER DO DRF (deve vir por último) =====
    path('', include(router.urls)),
] 