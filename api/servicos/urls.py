from django.urls import path
from . import views

urlpatterns = [
    path('', views.listar_servicos, name='listar_servicos'),
    path('<int:pk>/', views.servico_detalhe, name='servico_detalhe'),
] 