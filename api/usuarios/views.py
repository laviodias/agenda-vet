from django.shortcuts import render
from rest_framework import status, permissions, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .serializers import LoginSerializer, RegistroClienteSerializer, UsuarioSerializer, UsuarioCreateSerializer, DisponibilidadeProfissionalSerializer, DisponibilidadeProfissionalCreateSerializer
from .models import Usuario, DisponibilidadeProfissional
from core.permissions import PermissionChecker, require_permission, HasPermission
from django.db import transaction


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login(request):
    """
    Endpoint para login de usuários
    """
    serializer = LoginSerializer(data=request.data)
    
    if serializer.is_valid():
        user = serializer.validated_data['user']
        
        # Gerar tokens JWT
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'token': str(refresh.access_token),
            'refresh': str(refresh),
            'usuario': UsuarioSerializer(user).data
        })
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def registro_cliente(request):
    """
    Endpoint para registro de novos clientes
    """
    serializer = RegistroClienteSerializer(data=request.data)
    
    if serializer.is_valid():
        try:
            result = serializer.save()
            user = result['usuario']
            
            # Gerar tokens JWT
            refresh = RefreshToken.for_user(user)
            
            return Response({
                'token': str(refresh.access_token),
                'refresh': str(refresh),
                'usuario': UsuarioSerializer(user).data,
                'pet': result['pet'].nome
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response({
                'error': 'Erro ao criar usuário',
                'detail': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def perfil_usuario(request):
    """
    Endpoint para obter dados do usuário logado
    """
    return Response(UsuarioSerializer(request.user).data)


@api_view(['POST'])
def logout(request):
    """
    Endpoint para logout (invalidação de token)
    """
    try:
        refresh_token = request.data.get('refresh')
        if refresh_token:
            token = RefreshToken(refresh_token)
            token.blacklist()
        
        return Response({'message': 'Logout realizado com sucesso'})
    except Exception as e:
        return Response({'error': 'Erro ao fazer logout'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def listar_profissionais(request):
    """
    Lista todos os profissionais disponíveis
    """
    try:
        profissionais = Usuario.objects.filter(tipo='profissional', is_active=True)
        serializer = UsuarioSerializer(profissionais, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({
            'error': 'Erro ao buscar profissionais',
            'detail': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UsuarioViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciamento de usuários com controle de acesso baseado em roles
    """
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """
        Filtrar usuários baseado no role do usuário logado
        """
        user = self.request.user
        
        # Administradores veem todos os usuários
        if PermissionChecker.check_permission(user, 'usuarios', 'list'):
            return Usuario.objects.all()
        
        # Usuários normais só veem seus próprios dados
        return Usuario.objects.filter(id=user.id)
    
    def create(self, request, *args, **kwargs):
        # Verificar permissão para criar usuários
        if not PermissionChecker.check_permission(request.user, 'usuarios', 'create'):
            return PermissionChecker.get_permission_response('Você não tem permissão para criar usuários')
        return super().create(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        usuario = self.get_object()
        
        # Usuário pode editar seus próprios dados
        if usuario == request.user:
            return super().update(request, *args, **kwargs)
        
        # Administradores podem editar qualquer usuário
        if PermissionChecker.check_permission(request.user, 'usuarios', 'update'):
            return super().update(request, *args, **kwargs)
        
        return PermissionChecker.get_permission_response('Você não tem permissão para editar este usuário')
    
    def destroy(self, request, *args, **kwargs):
        usuario = self.get_object()
        
        # Usuário não pode deletar a si mesmo
        if usuario == request.user:
            return PermissionChecker.get_permission_response('Você não pode deletar sua própria conta')
        
        # Verificar permissão para deletar usuários
        if not PermissionChecker.check_permission(request.user, 'usuarios', 'delete'):
            return PermissionChecker.get_permission_response('Você não tem permissão para deletar usuários')
        
        return super().destroy(request, *args, **kwargs)

# ===== VIEWS PARA DISPONIBILIDADE DOS PROFISSIONAIS =====

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@require_permission('usuarios', 'read')
def get_disponibilidades_profissional(request, profissional_id):
    """Buscar disponibilidades de um profissional específico"""
    try:
        profissional = Usuario.objects.get(id=profissional_id, tipo='profissional')
        disponibilidades = DisponibilidadeProfissional.objects.filter(profissional=profissional, ativo=True)
        serializer = DisponibilidadeProfissionalSerializer(disponibilidades, many=True)
        return Response(serializer.data)
    except Usuario.DoesNotExist:
        return Response({'error': 'Profissional não encontrado'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@require_permission('usuarios', 'create')
def create_disponibilidade_profissional(request):
    """Criar disponibilidade para um profissional"""
    try:
        serializer = DisponibilidadeProfissionalCreateSerializer(data=request.data)
        if serializer.is_valid():
            disponibilidade = serializer.save()
            return Response(DisponibilidadeProfissionalSerializer(disponibilidade).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
@require_permission('usuarios', 'update')
def update_disponibilidade_profissional(request, disponibilidade_id):
    """Atualizar disponibilidade de um profissional"""
    try:
        disponibilidade = DisponibilidadeProfissional.objects.get(id=disponibilidade_id)
        serializer = DisponibilidadeProfissionalCreateSerializer(disponibilidade, data=request.data)
        if serializer.is_valid():
            disponibilidade = serializer.save()
            return Response(DisponibilidadeProfissionalSerializer(disponibilidade).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except DisponibilidadeProfissional.DoesNotExist:
        return Response({'error': 'Disponibilidade não encontrada'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
@require_permission('usuarios', 'delete')
def delete_disponibilidade_profissional(request, disponibilidade_id):
    """Deletar disponibilidade de um profissional"""
    try:
        disponibilidade = DisponibilidadeProfissional.objects.get(id=disponibilidade_id)
        disponibilidade.delete()
        return Response({'message': 'Disponibilidade deletada com sucesso'})
    except DisponibilidadeProfissional.DoesNotExist:
        return Response({'error': 'Disponibilidade não encontrada'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@require_permission('usuarios', 'update')
def bulk_update_disponibilidades(request, profissional_id):
    """Atualizar múltiplas disponibilidades de um profissional"""
    try:
        profissional = Usuario.objects.get(id=profissional_id, tipo='profissional')
        disponibilidades_data = request.data.get('disponibilidades', [])
        
        with transaction.atomic():
            # Deletar disponibilidades existentes
            DisponibilidadeProfissional.objects.filter(profissional=profissional).delete()
            
            # Criar novas disponibilidades
            for disp_data in disponibilidades_data:
                disp_data['profissional'] = profissional_id
                serializer = DisponibilidadeProfissionalCreateSerializer(data=disp_data)
                if serializer.is_valid():
                    serializer.save()
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # Retornar todas as disponibilidades do profissional
        disponibilidades = DisponibilidadeProfissional.objects.filter(profissional=profissional)
        serializer = DisponibilidadeProfissionalSerializer(disponibilidades, many=True)
        return Response(serializer.data)
        
    except Usuario.DoesNotExist:
        return Response({'error': 'Profissional não encontrado'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_profissionais_disponiveis(request):
    """Buscar profissionais disponíveis para um dia específico"""
    try:
        dia_semana = request.GET.get('dia_semana')
        if not dia_semana:
            return Response({'error': 'dia_semana é obrigatório'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Buscar profissionais com disponibilidade no dia
        disponibilidades = DisponibilidadeProfissional.objects.filter(
            dia_semana=dia_semana,
            ativo=True
        ).select_related('profissional')
        
        profissionais_disponiveis = []
        for disp in disponibilidades:
            profissionais_disponiveis.append({
                'id': disp.profissional.id,
                'nome': disp.profissional.nome,
                'especialidade': disp.profissional.especialidade,
                'hora_inicio': disp.hora_inicio,
                'hora_fim': disp.hora_fim
            })
        
        return Response(profissionais_disponiveis)
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
