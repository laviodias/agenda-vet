from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'empresas', views.EmpresaViewSet)
router.register(r'usuarios', views.UsuarioViewSet)
router.register(r'brand', views.ConfiguracaoBrandViewSet)
router.register(r'roles', views.RoleViewSet)
router.register(r'permissions', views.PermissionViewSet)
router.register(r'role-permissions', views.RolePermissionViewSet)
router.register(r'user-roles', views.UserRoleViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('dashboard/', views.dashboard_stats, name='dashboard_stats'),
    path('user-permissions/', views.user_permissions, name='user_permissions'),
    path('user-permissions/<int:user_id>/', views.user_permissions, name='user_permissions_detail'),
    path('can-access-admin/', views.can_access_admin, name='can_access_admin'),
] 