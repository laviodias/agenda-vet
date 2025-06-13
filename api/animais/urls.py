from django.urls import path
from . import views

urlpatterns = [
    path('', views.listar_pets, name='listar_pets'),
    path('criar/', views.criar_pet, name='criar_pet'),
    path('<int:pet_id>/', views.atualizar_pet, name='atualizar_pet'),
    path('<int:pet_id>/deletar/', views.deletar_pet, name='deletar_pet'),
] 