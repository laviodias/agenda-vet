from django.shortcuts import render
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from datetime import datetime, timedelta
from django.db.models import Count, Sum, Q
from django.db import transaction
from .models import Empresa, ConfiguracaoBrand, Role, Permission, RolePermission, UserRole
from agendamentos.models import Agendamento
from servicos.models import Servico
from .serializers import (EmpresaSerializer, ConfiguracaoBrandSerializer,
                         RoleSerializer, PermissionSerializer, RolePermissionSerializer, 
                         UserRoleSerializer, AssignRoleSerializer, UserPermissionsSerializer)
from .permissions import PermissionChecker, require_permission, HasPermission, require_role
from usuarios.models import Usuario
from usuarios.serializers import UsuarioSerializer

# Create your views here.

class EmpresaViewSet(viewsets.ModelViewSet):
    queryset = Empresa.objects.all()
    serializer_class = EmpresaSerializer

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [permissions.IsAuthenticated]


class ConfiguracaoBrandViewSet(viewsets.ModelViewSet):
    queryset = ConfiguracaoBrand.objects.all()
    serializer_class = ConfiguracaoBrandSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    
    def get_permissions(self):
        """
        Definir permissões baseadas no novo sistema de roles
        """
        if self.action == 'ativa':
            # Endpoint público para buscar configuração ativa
            permission_classes = [permissions.AllowAny]
        elif self.action in ['list', 'retrieve']:
            # Leitura requer permissão de visualizar configurações
            permission_classes = [permissions.IsAuthenticated]
        else:
            # Modificações requerem permissão específica
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def check_brand_permission(self, request, action):
        """
        Verificar se o usuário tem permissão para ações de marca/branding
        """
        if not request.user.is_authenticated:
            return False
        
        # Verificar se tem permissão específica para brand
        return PermissionChecker.check_permission(request.user, 'brand', action)
    
    @action(detail=False, methods=['get'])
    def ativa(self, request):
        """
        Endpoint para buscar a configuração de marca ativa
        """
        configuracao = ConfiguracaoBrand.get_configuracao_ativa()
        if configuracao:
            serializer = self.get_serializer(configuracao, context={'request': request})
            return Response(serializer.data)
        return Response({'message': 'Nenhuma configuração encontrada'}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=True, methods=['post'])
    def ativar(self, request, pk=None):
        """
        Endpoint para ativar uma configuração específica
        """
        configuracao = self.get_object()
        # Desativar todas as outras configurações
        ConfiguracaoBrand.objects.filter(ativo=True).update(ativo=False)
        # Ativar a configuração selecionada
        configuracao.ativo = True
        configuracao.save()
        
        serializer = self.get_serializer(configuracao, context={'request': request})
        return Response({
            'message': 'Configuração ativada com sucesso',
            'configuracao': serializer.data
        })
    
    @action(detail=True, methods=['patch'], parser_classes=[MultiPartParser, FormParser])
    def upload_logo(self, request, pk=None):
        """
        Endpoint específico para upload de logo
        """
        # Verificar permissão para atualizar marca
        if not self.check_brand_permission(request, 'update'):
            return PermissionChecker.get_permission_response('Você não tem permissão para fazer upload de logo')
        
        configuracao = self.get_object()
        
        print(f"Request FILES: {request.FILES}")
        print(f"Request content type: {request.content_type}")
        
        if 'logo' not in request.FILES:
            return Response({'error': 'Nenhum arquivo foi enviado'}, status=status.HTTP_400_BAD_REQUEST)
        
        logo_file = request.FILES['logo']
        
        print(f"Logo file: {logo_file}")
        print(f"Logo file size: {logo_file.size}")
        print(f"Logo file content type: {logo_file.content_type}")
        
        # Validar arquivo
        if logo_file.size > 2 * 1024 * 1024:
            return Response({'error': 'Arquivo muito grande. Máximo 2MB.'}, status=status.HTTP_400_BAD_REQUEST)
        
        allowed_types = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif']
        if logo_file.content_type not in allowed_types:
            return Response({'error': 'Tipo de arquivo não permitido. Use JPG, PNG ou GIF.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Salvar o arquivo
        configuracao.logo = logo_file
        configuracao.save()
        
        print(f"Logo saved successfully: {configuracao.logo.url}")
        
        serializer = self.get_serializer(configuracao, context={'request': request})
        return Response({
            'message': 'Logo atualizado com sucesso',
            'configuracao': serializer.data
        })
    
    def create(self, request, *args, **kwargs):
        """
        Sobrescrever create para automaticamente desativar outras configurações
        """
        # Verificar permissão para criar configurações de marca
        if not self.check_brand_permission(request, 'create'):
            return PermissionChecker.get_permission_response('Você não tem permissão para criar configurações de marca')
        
        # Se a nova configuração está sendo marcada como ativa, desativar outras
        if request.data.get('ativo', False):
            ConfiguracaoBrand.objects.filter(ativo=True).update(ativo=False)
        
        return super().create(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        """
        Sobrescrever update para gerenciar ativação e upload de arquivos
        """
        # Verificar permissão para atualizar configurações de marca
        if not self.check_brand_permission(request, 'update'):
            return PermissionChecker.get_permission_response('Você não tem permissão para atualizar configurações de marca')
        
        instance = self.get_object()
        
        # Log para debug
        print(f"Update request data: {request.data}")
        print(f"Files: {request.FILES}")
        
        # Se está ativando esta configuração, desativar outras
        if request.data.get('ativo', False) and not instance.ativo:
            ConfiguracaoBrand.objects.filter(ativo=True).update(ativo=False)
        
        # Se é um upload de arquivo, usar partial=True
        partial = kwargs.pop('partial', False)
        if 'logo' in request.FILES:
            partial = True
            
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)
    
    def destroy(self, request, *args, **kwargs):
        """
        Sobrescrever delete para verificar permissões
        """
        # Verificar permissão para deletar configurações de marca
        if not self.check_brand_permission(request, 'delete'):
            return PermissionChecker.get_permission_response('Você não tem permissão para deletar configurações de marca')
        
        return super().destroy(request, *args, **kwargs)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def info_clinica(request):
    """
    Retorna informações da clínica
    """
    try:
        empresa = Empresa.objects.first()
        if not empresa:
            empresa = Empresa.objects.create(
                nome='AgendaVet',
                cnpj='00.000.000/0001-00',
                endereco='Rua das Flores, 123 - Centro',
                telefone='(11) 99999-9999'
            )
        
        return Response({
            'nome': empresa.nome,
            'endereco': empresa.endereco,
            'telefone': empresa.telefone,
            'email': 'contato@agendavet.com',
            'descricao': 'Clínica veterinária especializada no cuidado e bem-estar dos seus pets.',
            'sobre': 'Com mais de 10 anos de experiência, nossa clínica oferece atendimento de qualidade com profissionais especializados e equipamentos modernos.'
        })
    except Exception as e:
        return Response({
            'error': 'Erro ao buscar informações da clínica',
            'detail': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def horarios_funcionamento(request):
    """
    Retorna horários de funcionamento da clínica
    """
    try:
        return Response({
            'segunda': {'inicio': '08:00', 'fim': '18:00', 'aberto': True},
            'terca': {'inicio': '08:00', 'fim': '18:00', 'aberto': True},
            'quarta': {'inicio': '08:00', 'fim': '18:00', 'aberto': True},
            'quinta': {'inicio': '08:00', 'fim': '18:00', 'aberto': True},
            'sexta': {'inicio': '08:00', 'fim': '18:00', 'aberto': True},
            'sabado': {'inicio': '08:00', 'fim': '12:00', 'aberto': True},
            'domingo': {'inicio': '00:00', 'fim': '00:00', 'aberto': False}
        })
    except Exception as e:
        return Response({
            'error': 'Erro ao buscar horários de funcionamento',
            'detail': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
@require_role('admin')
def dashboard_stats(request):
    """
    Retorna estatísticas do dashboard para admin
    """
    try:
        hoje = timezone.now().date()
        inicio_mes = hoje.replace(day=1)
        
        # Estatísticas básicas
        total_agendamentos = Agendamento.objects.count()
        agendamentos_hoje = Agendamento.objects.filter(data_hora__date=hoje).count()
        agendamentos_pendentes = Agendamento.objects.filter(data_hora__gt=timezone.now()).count()
        
        # Faturamento do mês
        faturamento_mes = Agendamento.objects.filter(
            data_hora__date__gte=inicio_mes
        ).aggregate(
            total=Sum('servico__preco')
        )['total'] or 0
        
        # Clientes ativos (que fizeram agendamento nos últimos 30 dias)
        clientes_ativos = Usuario.objects.filter(
            agendamentos_cliente__data_hora__gte=timezone.now() - timedelta(days=30),
            tipo='cliente'
        ).distinct().count()
        
        # Serviços mais populares
        servicos_populares = Servico.objects.annotate(
            quantidade=Count('agendamentos')
        ).order_by('-quantidade')[:5]
        
        servicos_data = [
            {
                'nome': servico.nome,
                'quantidade': servico.quantidade
            }
            for servico in servicos_populares
        ]
        
        return Response({
            'totalAgendamentos': total_agendamentos,
            'agendamentosHoje': agendamentos_hoje,
            'agendamentosPendentes': agendamentos_pendentes,
            'faturamentoMes': float(faturamento_mes),
            'clientesAtivos': clientes_ativos,
            'servicosPopulares': servicos_data
        })
        
    except Exception as e:
        return Response({
            'error': 'Erro ao buscar estatísticas',
            'detail': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
@require_role('admin')
def agendamentos_recentes(request):
    """
    Retorna agendamentos recentes para o dashboard
    """
    try:
        agendamentos = Agendamento.objects.select_related(
            'servico', 'animal', 'cliente', 'responsavel'
        ).order_by('-data_hora')[:10]
        
        data = []
        for agendamento in agendamentos:
            data.append({
                'id': agendamento.id,
                'data_hora': agendamento.data_hora.isoformat(),
                'servico': agendamento.servico.nome,
                'preco': float(agendamento.servico.preco),
                'pet': agendamento.animal.nome,
                'cliente': agendamento.cliente.nome,
                'profissional': agendamento.responsavel.nome if agendamento.responsavel else 'Não definido',
                'observacoes': agendamento.observacoes or '',
                'status': 'confirmado'  # Status fixo por enquanto
            })
        
        return Response(data)
        
    except Exception as e:
        return Response({
            'error': 'Erro ao buscar agendamentos recentes',
            'detail': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class RoleViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciamento de roles
    """
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_permissions(self):
        """
        Apenas administradores podem gerenciar roles
        """
        if self.action in ['list', 'retrieve']:
            # Leitura para usuários autenticados
            permission_classes = [permissions.IsAuthenticated]
        else:
            # Modificações apenas para admins
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def create(self, request, *args, **kwargs):
        # Verificar permissão para gerenciar usuários
        if not PermissionChecker.check_permission(request.user, 'usuarios', 'manage'):
            return PermissionChecker.get_permission_response('Você não tem permissão para criar roles')
        return super().create(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        # Verificar permissão para gerenciar usuários
        if not PermissionChecker.check_permission(request.user, 'usuarios', 'manage'):
            return PermissionChecker.get_permission_response('Você não tem permissão para editar roles')
        return super().update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        # Verificar permissão para gerenciar usuários
        if not PermissionChecker.check_permission(request.user, 'usuarios', 'manage'):
            return PermissionChecker.get_permission_response('Você não tem permissão para deletar roles')
        
        role = self.get_object()
        # Verificar se há usuários usando este role
        if role.user_assignments.filter(is_active=True).exists():
            return Response({
                'error': 'Não é possível deletar role que está sendo usado por usuários',
                'users_count': role.user_assignments.filter(is_active=True).count()
            }, status=status.HTTP_400_BAD_REQUEST)
        
        return super().destroy(request, *args, **kwargs)


class PermissionViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet para visualização de permissões (somente leitura)
    """
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_permissions(self):
        """
        Permissões de visualização para usuários autenticados
        """
        return [permissions.IsAuthenticated()]


class RolePermissionViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciar atribuições de permissões aos roles
    """
    queryset = RolePermission.objects.all()
    serializer_class = RolePermissionSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        # Verificar permissão para gerenciar usuários
        if not PermissionChecker.check_permission(request.user, 'usuarios', 'manage'):
            return PermissionChecker.get_permission_response('Você não tem permissão para atribuir permissões')
        return super().create(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        # Verificar permissão para gerenciar usuários
        if not PermissionChecker.check_permission(request.user, 'usuarios', 'manage'):
            return PermissionChecker.get_permission_response('Você não tem permissão para remover permissões')
        return super().destroy(request, *args, **kwargs)


class UserRoleViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciar atribuições de roles aos usuários
    """
    queryset = UserRole.objects.all()
    serializer_class = UserRoleSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """
        Filtrar baseado nas permissões do usuário
        """
        user = self.request.user
        
        # Administradores veem todas as atribuições
        if PermissionChecker.check_permission(user, 'usuarios', 'list'):
            return UserRole.objects.all()
        
        # Usuários normais veem apenas suas próprias atribuições
        return UserRole.objects.filter(user=user)
    
    def create(self, request, *args, **kwargs):
        # Verificar permissão para gerenciar usuários
        if not PermissionChecker.check_permission(request.user, 'usuarios', 'manage'):
            return PermissionChecker.get_permission_response('Você não tem permissão para atribuir roles')
        return super().create(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        # Verificar permissão para gerenciar usuários
        if not PermissionChecker.check_permission(request.user, 'usuarios', 'manage'):
            return PermissionChecker.get_permission_response('Você não tem permissão para editar atribuições de roles')
        return super().update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        user_role = self.get_object()
        
        # Usuário pode remover seus próprios roles (para sair de funções)
        if user_role.user == request.user:
            return super().destroy(request, *args, **kwargs)
        
        # Administradores podem remover qualquer atribuição
        if not PermissionChecker.check_permission(request.user, 'usuarios', 'manage'):
            return PermissionChecker.get_permission_response('Você não tem permissão para remover roles de outros usuários')
        
        return super().destroy(request, *args, **kwargs)
    
    @action(detail=False, methods=['post'])
    def assign_role(self, request):
        """
        Endpoint para atribuir role a um usuário
        """
        if not PermissionChecker.check_permission(request.user, 'usuarios', 'manage'):
            return PermissionChecker.get_permission_response('Você não tem permissão para atribuir roles')
        
        serializer = AssignRoleSerializer(data=request.data)
        if serializer.is_valid():
            user_id = serializer.validated_data['user_id']
            role_id = serializer.validated_data['role_id']
            
            user = Usuario.objects.get(id=user_id)
            role = Role.objects.get(id=role_id)
            
            # Usar o método do modelo para atribuir role
            user_role = user.assign_role(role.name, assigned_by=request.user)
            
            if user_role:
                response_serializer = UserRoleSerializer(user_role, context={'request': request})
                return Response({
                    'message': f'Role {role.display_name} atribuído com sucesso para {user.nome}',
                    'user_role': response_serializer.data
                }, status=status.HTTP_201_CREATED)
            else:
                return Response({
                    'error': 'Não foi possível atribuir o role'
                }, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'])
    def remove_role(self, request):
        """
        Endpoint para remover role de um usuário
        """
        if not PermissionChecker.check_permission(request.user, 'usuarios', 'manage'):
            return PermissionChecker.get_permission_response('Você não tem permissão para remover roles')
        
        user_id = request.data.get('user_id')
        role_name = request.data.get('role_name')
        
        if not user_id or not role_name:
            return Response({
                'error': 'user_id e role_name são obrigatórios'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = Usuario.objects.get(id=user_id)
            user.remove_role(role_name)
            
            return Response({
                'message': f'Role {role_name} removido com sucesso de {user.nome}'
            })
        except Usuario.DoesNotExist:
            return Response({
                'error': 'Usuário não encontrado'
            }, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_permissions(request, user_id=None):
    """
    Listar permissões de um usuário específico
    """
    if user_id is None:
        user = request.user
    else:
        # Verificar se pode ver permissões de outros usuários
        if not PermissionChecker.check_permission(request.user, 'usuarios', 'read') and request.user.id != user_id:
            return PermissionChecker.get_permission_response('Você não tem permissão para ver permissões de outros usuários')
        
        try:
            user = Usuario.objects.get(id=user_id)
        except Usuario.DoesNotExist:
            return Response({
                'error': 'Usuário não encontrado'
            }, status=status.HTTP_404_NOT_FOUND)
    
    roles = user.get_roles()
    permissions = user.get_permissions()
    
    return Response({
        'user': {
            'id': user.id,
            'nome': user.nome,
            'email': user.email,
            'tipo_usuario': user.tipo_usuario
        },
        'roles': [{'name': role.name, 'display_name': role.display_name, 'description': role.description} for role in roles],
        'permissions': [{'resource': perm.resource, 'action': perm.action, 'description': perm.description, 'codename': perm.codename} for perm in permissions],
        'total_roles': roles.count(),
        'total_permissions': permissions.count()
    })


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def can_access_admin(request):
    """
    Retorna se o usuário autenticado pode acessar a área admin (tem role admin)
    """
    user = request.user
    print(f"[can_access_admin] Usuário autenticado: {user} (id={user.id}, email={getattr(user, 'email', None)})")
    has_admin = False
    if hasattr(user, 'has_role'):
        has_admin = user.has_role('admin')
    print(f"[can_access_admin] has_role('admin') = {has_admin}")
    return Response({'can_access_admin': has_admin})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@require_permission('usuarios', 'read')
def get_roles(request):
    """Listar todos os roles"""
    include_inactive = request.GET.get('include_inactive', 'false').lower() == 'true'
    
    if include_inactive:
        roles = Role.objects.all().prefetch_related('permissions__permission')
    else:
        roles = Role.objects.filter(is_active=True).prefetch_related('permissions__permission')
    
    serializer = RoleSerializer(roles, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@require_permission('usuarios', 'create')
def create_role(request):
    """Criar novo role"""
    try:
        with transaction.atomic():
            role_data = {
                'name': request.data.get('name'),
                'display_name': request.data.get('display_name'),
                'description': request.data.get('description', ''),
                'is_active': True
            }
            
            role = Role.objects.create(**role_data)
            
            # Atribuir permissões
            permissions = request.data.get('permissions', [])
            for perm_id in permissions:
                try:
                    permission = Permission.objects.get(id=perm_id)
                    RolePermission.objects.create(
                        role=role,
                        permission=permission,
                        granted_by=request.user
                    )
                except Permission.DoesNotExist:
                    continue
            
            serializer = RoleSerializer(role)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
@require_permission('usuarios', 'update')
def update_role(request, role_id):
    """Atualizar role"""
    try:
        role = Role.objects.get(id=role_id)
        
        role.name = request.data.get('name', role.name)
        role.display_name = request.data.get('display_name', role.display_name)
        role.description = request.data.get('description', role.description)
        role.save()
        
        serializer = RoleSerializer(role)
        return Response(serializer.data)
        
    except Role.DoesNotExist:
        return Response({'error': 'Role não encontrado'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
@require_permission('usuarios', 'delete')
def delete_role(request, role_id):
    """Deletar role"""
    try:
        role = Role.objects.get(id=role_id)
        role.is_active = False
        role.save()
        return Response({'message': 'Role desativado com sucesso'})
        
    except Role.DoesNotExist:
        return Response({'error': 'Role não encontrado'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
@require_permission('usuarios', 'update')
def toggle_role_status(request, role_id):
    """Ativar/desativar role"""
    try:
        role = Role.objects.get(id=role_id)
        role.is_active = not role.is_active
        role.save()
        
        status_text = 'ativado' if role.is_active else 'desativado'
        return Response({'message': f'Role {status_text} com sucesso'})
        
    except Role.DoesNotExist:
        return Response({'error': 'Role não encontrado'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@require_permission('usuarios', 'read')
def get_permissions(request):
    """Listar todas as permissões"""
    permissions = Permission.objects.all().order_by('resource', 'action')
    serializer = PermissionSerializer(permissions, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@require_permission('usuarios', 'update')
def assign_permissions(request, role_id):
    """Atribuir permissões a um role"""
    try:
        role = Role.objects.get(id=role_id)
        permissions = request.data.get('permissions', [])
        
        with transaction.atomic():
            # Limpar permissões existentes
            RolePermission.objects.filter(role=role).delete()
            
            # Adicionar novas permissões
            for perm_id in permissions:
                try:
                    permission = Permission.objects.get(id=perm_id)
                    RolePermission.objects.create(
                        role=role,
                        permission=permission,
                        granted_by=request.user
                    )
                except Permission.DoesNotExist:
                    continue
        
        return Response({'message': 'Permissões atualizadas com sucesso'})
        
    except Role.DoesNotExist:
        return Response({'error': 'Role não encontrado'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@require_permission('usuarios', 'read')
def get_users(request):
    """Listar usuários para atribuição de roles"""
    users = Usuario.objects.filter(is_active=True).order_by('nome')
    data = []
    for user in users:
        data.append({
            'id': user.id,
            'nome': user.nome,
            'email': user.email,
            'tipo': user.get_tipo_display()
        })
    return Response(data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@require_permission('usuarios', 'update')
def assign_user_roles(request):
    """Atribuir roles a um usuário"""
    try:
        user_id = request.data.get('user_id')
        roles = request.data.get('roles', [])
        
        if not user_id:
            return Response({'error': 'user_id é obrigatório'}, status=status.HTTP_400_BAD_REQUEST)
        
        user = Usuario.objects.get(id=user_id)
        
        with transaction.atomic():
            # Limpar roles existentes
            UserRole.objects.filter(user=user).delete()
            
            # Adicionar novos roles
            for role_id in roles:
                try:
                    role = Role.objects.get(id=role_id, is_active=True)
                    UserRole.objects.create(
                        user=user,
                        role=role,
                        assigned_by=request.user
                    )
                except Role.DoesNotExist:
                    continue
        
        return Response({'message': 'Roles atribuídos com sucesso'})
        
    except Usuario.DoesNotExist:
        return Response({'error': 'Usuário não encontrado'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@require_permission('usuarios', 'read')
def get_role_stats(request):
    """Buscar estatísticas de roles"""
    try:
        roles_count = Role.objects.filter(is_active=True).count()
        permissions_count = Permission.objects.count()
        users_count = Usuario.objects.filter(is_active=True).count()
        assignments_count = UserRole.objects.filter(is_active=True).count()
        
        return Response({
            'rolesCount': roles_count,
            'permissionsCount': permissions_count,
            'usersCount': users_count,
            'assignmentsCount': assignments_count
        })
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


# ===== VIEWS PARA CONFIGURAÇÕES DE MARCA =====

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_brand_config(request):
    """Buscar configuração de marca ativa"""
    try:
        configuracao = ConfiguracaoBrand.get_configuracao_ativa()
        if configuracao:
            serializer = ConfiguracaoBrandSerializer(configuracao, context={'request': request})
            return Response(serializer.data)
        return Response({'message': 'Nenhuma configuração encontrada'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@require_permission('brand', 'read')
def brand_config_list(request):
    """Listar todas as configurações de marca"""
    try:
        configs = ConfiguracaoBrand.objects.all().order_by('-criado_em')
        serializer = ConfiguracaoBrandSerializer(configs, many=True, context={'request': request})
        return Response(serializer.data)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
@require_permission('brand', 'read')
def brand_config_detail(request, pk):
    """Detalhes de uma configuração específica"""
    try:
        config = ConfiguracaoBrand.objects.get(pk=pk)
        
        if request.method == 'GET':
            serializer = ConfiguracaoBrandSerializer(config, context={'request': request})
            return Response(serializer.data)
        
        elif request.method == 'PUT':
            if not PermissionChecker.check_permission(request.user, 'brand', 'update'):
                return Response({'error': 'Sem permissão para atualizar'}, status=status.HTTP_403_FORBIDDEN)
            
            serializer = ConfiguracaoBrandSerializer(config, data=request.data, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        elif request.method == 'DELETE':
            if not PermissionChecker.check_permission(request.user, 'brand', 'delete'):
                return Response({'error': 'Sem permissão para deletar'}, status=status.HTTP_403_FORBIDDEN)
            
            config.delete()
            return Response({'message': 'Configuração deletada com sucesso'})
            
    except ConfiguracaoBrand.DoesNotExist:
        return Response({'error': 'Configuração não encontrada'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@require_permission('brand', 'update')
def activate_brand_config(request, pk):
    """Ativar uma configuração de marca"""
    try:
        config = ConfiguracaoBrand.objects.get(pk=pk)
        
        # Desativar todas as outras configurações
        ConfiguracaoBrand.objects.filter(ativo=True).update(ativo=False)
        
        # Ativar a configuração selecionada
        config.ativo = True
        config.save()
        
        serializer = ConfiguracaoBrandSerializer(config, context={'request': request})
        return Response({
            'message': 'Configuração ativada com sucesso',
            'configuracao': serializer.data
        })
        
    except ConfiguracaoBrand.DoesNotExist:
        return Response({'error': 'Configuração não encontrada'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@require_permission('usuarios', 'read')
def get_user_roles(request, user_id):
    """Buscar roles de um usuário específico"""
    try:
        user = Usuario.objects.get(id=user_id)
        user_roles = UserRole.objects.filter(user=user).select_related('role')
        serializer = UserRoleSerializer(user_roles, many=True)
        return Response(serializer.data)
    except Usuario.DoesNotExist:
        return Response({'error': 'Usuário não encontrado'}, status=404)
    except Exception as e:
        return Response({'error': str(e)}, status=500)
