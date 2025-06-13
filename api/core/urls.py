from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EmpresaViewSet
from . import views

router = DefaultRouter()
router.register(r'empresas', EmpresaViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('clinica/info/', views.info_clinica, name='info_clinica'),
    path('horarios-funcionamento/', views.horarios_funcionamento, name='horarios_funcionamento'),
    path('admin/dashboard/stats/', views.dashboard_stats, name='dashboard_stats'),
    path('admin/agendamentos/recentes/', views.agendamentos_recentes, name='agendamentos_recentes'),
] 