from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'empresas', views.EmpresaViewSet)
router.register(r'usuarios', views.UsuarioViewSet)
router.register(r'brand', views.ConfiguracaoBrandViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('dashboard/', views.dashboard_stats, name='dashboard_stats'),
] 