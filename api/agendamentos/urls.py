from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DisponibilidadeAgendaViewSet, AgendamentoViewSet

router = DefaultRouter()
router.register(r'disponibilidades', DisponibilidadeAgendaViewSet)
router.register(r'agendamentos', AgendamentoViewSet)

urlpatterns = [
    path('', include(router.urls)),
] 