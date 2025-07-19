from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'usuarios', views.UsuarioViewSet)

urlpatterns = [
    path('auth/login/', views.login, name='login'),
    path('auth/register/cliente/', views.registro_cliente, name='registro_cliente'),
    path('auth/logout/', views.logout, name='logout'),
    path('auth/me/', views.perfil_usuario, name='auth_me'),  # Endpoint para dados do usuário logado
    path('perfil/', views.perfil_usuario, name='perfil_usuario'),
    path('', include(router.urls)),
] 