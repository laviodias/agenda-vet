from django.shortcuts import render
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import Servico
from .serializers import ServicoSerializer
from core.permissions import PermissionChecker, require_permission, HasPermission

# Create your views here.

class ServicoViewSet(viewsets.ModelViewSet):
    queryset = Servico.objects.all()
    serializer_class = ServicoSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_permissions(self):
        """
        Definir permissões baseadas no sistema de roles
        """
        if self.action in ['list', 'retrieve']:
            # Leitura de serviços é pública
            permission_classes = [permissions.AllowAny]
        else:
            # Modificações requerem permissão específica
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def create(self, request, *args, **kwargs):
        # Verificar permissão para criar serviços
        if not PermissionChecker.check_permission(request.user, 'servicos', 'create'):
            return PermissionChecker.get_permission_response('Você não tem permissão para criar serviços')
        return super().create(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        # Verificar permissão para atualizar serviços
        if not PermissionChecker.check_permission(request.user, 'servicos', 'update'):
            return PermissionChecker.get_permission_response('Você não tem permissão para atualizar serviços')
        return super().update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        # Verificar permissão para deletar serviços
        if not PermissionChecker.check_permission(request.user, 'servicos', 'delete'):
            return PermissionChecker.get_permission_response('Você não tem permissão para deletar serviços')
        return super().destroy(request, *args, **kwargs)

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def listar_servicos(request):
    """
    Lista todos os serviços disponíveis
    """
    try:
        servicos = Servico.objects.all()
        serializer = ServicoSerializer(servicos, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({
            'error': 'Erro ao buscar serviços',
            'detail': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def servico_detalhe(request, pk):
    """
    Retorna detalhes de um serviço específico
    """
    try:
        servico = Servico.objects.get(pk=pk)
        serializer = ServicoSerializer(servico)
        return Response(serializer.data)
    except Servico.DoesNotExist:
        return Response({
            'error': 'Serviço não encontrado'
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({
            'error': 'Erro ao buscar serviço',
            'detail': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
