from django.urls import path
from . import views

urlpatterns = [
    path('auth/login/', views.login, name='login'),
    path('auth/register/cliente/', views.registro_cliente, name='registro_cliente'),
    path('auth/logout/', views.logout, name='logout'),
    path('perfil/', views.perfil_usuario, name='perfil_usuario'),
    path('profissionais/', views.listar_profissionais, name='listar_profissionais'),
] 