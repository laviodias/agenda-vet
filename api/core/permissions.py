from django.http import JsonResponse
from django.core.exceptions import PermissionDenied
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from functools import wraps
from .models import Permission, Role, UserRole


class RoleBasedPermission(permissions.BasePermission):
    """
    Classe base para verificação de permissões baseada em roles
    """
    
    def __init__(self, resource=None, action=None, required_roles=None):
        self.resource = resource
        self.action = action
        self.required_roles = required_roles or []
    
    def has_permission(self, request, view):
        # Usuários não autenticados não têm permissão
        if not request.user or not request.user.is_authenticated:
            return False
        
        # Superusuários sempre têm permissão
        if request.user.is_superuser:
            return True
        
        # Se foram especificados roles obrigatórios, verificar
        if self.required_roles:
            user_has_role = any(
                request.user.has_role(role) for role in self.required_roles
            )
            if not user_has_role:
                return False
        
        # Se foram especificados resource e action, verificar permissão específica
        if self.resource and self.action:
            return request.user.has_permission(self.resource, self.action)
        
        return True


def require_permission(resource, action):
    """
    Decorator para views que requer uma permissão específica
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return JsonResponse({'error': 'Usuário não autenticado'}, status=401)
            
            if not request.user.has_permission(resource, action):
                return JsonResponse({
                    'error': 'Permissão negada',
                    'required_permission': f"{action}_{resource}"
                }, status=403)
            
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator


def require_role(role_name):
    """
    Decorator para views que requer um role específico
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return JsonResponse({'error': 'Usuário não autenticado'}, status=401)
            
            if not request.user.has_role(role_name):
                return JsonResponse({
                    'error': 'Role insuficiente',
                    'required_role': role_name
                }, status=403)
            
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator


def require_roles(*role_names):
    """
    Decorator para views que requer um ou mais roles específicos (OR logic)
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return JsonResponse({'error': 'Usuário não autenticado'}, status=401)
            
            user_has_role = any(
                request.user.has_role(role) for role in role_names
            )
            
            if not user_has_role:
                return JsonResponse({
                    'error': 'Role insuficiente',
                    'required_roles': list(role_names)
                }, status=403)
            
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator


class HasPermission(permissions.BasePermission):
    """
    Permission class para DRF ViewSets que verifica permissão específica
    """
    
    def __init__(self, resource, action):
        self.resource = resource
        self.action = action
    
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        if request.user.is_superuser:
            return True
        
        return request.user.has_permission(self.resource, self.action)


class HasRole(permissions.BasePermission):
    """
    Permission class para DRF ViewSets que verifica role específico
    """
    
    def __init__(self, role_name):
        self.role_name = role_name
    
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        if request.user.is_superuser:
            return True
        
        return request.user.has_role(self.role_name)


class HasAnyRole(permissions.BasePermission):
    """
    Permission class para DRF ViewSets que verifica se o usuário tem qualquer um dos roles
    """
    
    def __init__(self, *role_names):
        self.role_names = role_names
    
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        if request.user.is_superuser:
            return True
        
        return any(request.user.has_role(role) for role in self.role_names)


class PermissionChecker:
    """
    Classe utilitária para verificação de permissões em ViewSets
    """
    
    @staticmethod
    def check_permission(user, resource, action):
        """
        Verifica se um usuário tem uma permissão específica
        """
        if not user or not user.is_authenticated:
            return False
        
        if user.is_superuser:
            return True
        
        return user.has_permission(resource, action)
    
    @staticmethod
    def check_role(user, role_name):
        """
        Verifica se um usuário tem um role específico
        """
        if not user or not user.is_authenticated:
            return False
        
        if user.is_superuser:
            return True
        
        return user.has_role(role_name)
    
    @staticmethod
    def get_permission_response(message="Permissão negada"):
        """
        Retorna uma resposta padrão para erro de permissão
        """
        return Response({
            'error': message,
            'code': 'PERMISSION_DENIED'
        }, status=status.HTTP_403_FORBIDDEN)


def get_action_from_method(method):
    """
    Mapeia métodos HTTP para ações de permissão
    """
    action_mapping = {
        'GET': 'read',
        'POST': 'create',
        'PUT': 'update',
        'PATCH': 'update',
        'DELETE': 'delete',
    }
    return action_mapping.get(method.upper(), 'read')


def auto_permission_check(resource):
    """
    Decorator que automaticamente verifica permissões baseado no método HTTP
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return JsonResponse({'error': 'Usuário não autenticado'}, status=401)
            
            action = get_action_from_method(request.method)
            
            if not request.user.has_permission(resource, action):
                return JsonResponse({
                    'error': 'Permissão negada',
                    'required_permission': f"{action}_{resource}"
                }, status=403)
            
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator 