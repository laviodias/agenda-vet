from django.shortcuts import render
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.utils import timezone
from datetime import datetime, timedelta
from .models import DisponibilidadeAgenda, Agendamento
from .serializers import DisponibilidadeAgendaSerializer, AgendamentoSerializer
from servicos.models import Servico
from usuarios.models import Usuario
from core.permissions import PermissionChecker, require_permission, HasPermission

# Create your views here.

class DisponibilidadeAgendaViewSet(viewsets.ModelViewSet):
    queryset = DisponibilidadeAgenda.objects.all()
    serializer_class = DisponibilidadeAgendaSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_permissions(self):
        """
        Definir permissões baseadas no sistema de roles
        """
        if self.action in ['list', 'retrieve']:
            # Leitura de disponibilidade pode ser feita por qualquer usuário autenticado
            permission_classes = [permissions.IsAuthenticated]
        else:
            # Modificações requerem permissão específica
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def create(self, request, *args, **kwargs):
        # Verificar permissão para gerenciar agendamentos
        if not PermissionChecker.check_permission(request.user, 'agendamentos', 'manage'):
            return PermissionChecker.get_permission_response('Você não tem permissão para gerenciar disponibilidade')
        return super().create(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        # Verificar permissão para gerenciar agendamentos
        if not PermissionChecker.check_permission(request.user, 'agendamentos', 'manage'):
            return PermissionChecker.get_permission_response('Você não tem permissão para gerenciar disponibilidade')
        return super().update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        # Verificar permissão para gerenciar agendamentos
        if not PermissionChecker.check_permission(request.user, 'agendamentos', 'manage'):
            return PermissionChecker.get_permission_response('Você não tem permissão para gerenciar disponibilidade')
        return super().destroy(request, *args, **kwargs)


class AgendamentoViewSet(viewsets.ModelViewSet):
    queryset = Agendamento.objects.all()
    serializer_class = AgendamentoSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """
        Filtrar agendamentos baseado no role do usuário
        """
        user = self.request.user
        
        # Admins e profissionais veem todos os agendamentos
        if PermissionChecker.check_permission(user, 'agendamentos', 'list'):
            return Agendamento.objects.all()
        
        # Clientes veem apenas seus próprios agendamentos
        return Agendamento.objects.filter(cliente=user)
    
    def create(self, request, *args, **kwargs):
        # Qualquer usuário autenticado pode criar agendamento
        return super().create(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        agendamento = self.get_object()
        
        # Cliente pode editar apenas seus próprios agendamentos
        if agendamento.cliente == request.user:
            return super().update(request, *args, **kwargs)
        
        # Profissionais/admins podem editar qualquer agendamento
        if PermissionChecker.check_permission(request.user, 'agendamentos', 'update'):
            return super().update(request, *args, **kwargs)
        
        return PermissionChecker.get_permission_response('Você não tem permissão para editar este agendamento')
    
    def destroy(self, request, *args, **kwargs):
        agendamento = self.get_object()
        
        # Cliente pode cancelar apenas seus próprios agendamentos
        if agendamento.cliente == request.user:
            return super().destroy(request, *args, **kwargs)
        
        # Profissionais/admins podem cancelar qualquer agendamento
        if PermissionChecker.check_permission(request.user, 'agendamentos', 'delete'):
            return super().destroy(request, *args, **kwargs)
        
        return PermissionChecker.get_permission_response('Você não tem permissão para cancelar este agendamento')

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def listar_agendamentos_cliente(request):
    """
    Lista agendamentos do cliente logado
    """
    try:
        agendamentos = Agendamento.objects.filter(cliente=request.user).order_by('-data_hora')
        serializer = AgendamentoSerializer(agendamentos, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({
            'error': 'Erro ao buscar agendamentos',
            'detail': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def listar_todos_agendamentos(request):
    """
    Lista todos os agendamentos (admin/profissional)
    """
    try:
        agendamentos = Agendamento.objects.all().order_by('-data_hora')
        serializer = AgendamentoSerializer(agendamentos, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({
            'error': 'Erro ao buscar agendamentos',
            'detail': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def criar_agendamento(request):
    """
    Cria um novo agendamento
    """
    try:
        data = request.data.copy()
        data['cliente'] = request.user.id
        
        # Verificar se a data/hora está disponível
        data_hora = datetime.fromisoformat(data['data_hora'].replace('Z', '+00:00'))
        
        # Verificar se já existe agendamento no mesmo horário
        agendamento_existente = Agendamento.objects.filter(
            data_hora=data_hora,
            responsavel=data.get('responsavel')
        ).exists()
        
        if agendamento_existente:
            return Response({
                'error': 'Horário não disponível'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = AgendamentoSerializer(data=data)
        if serializer.is_valid():
            agendamento = serializer.save()
            return Response(AgendamentoSerializer(agendamento).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    except Exception as e:
        return Response({
            'error': 'Erro ao criar agendamento',
            'detail': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['PATCH'])
@permission_classes([permissions.IsAuthenticated])
def confirmar_agendamento(request, agendamento_id):
    """
    Confirma um agendamento (admin/profissional)
    """
    try:
        agendamento = Agendamento.objects.get(id=agendamento_id)
        # Aqui você pode adicionar lógica adicional para confirmação
        return Response({'message': 'Agendamento confirmado com sucesso'})
    except Agendamento.DoesNotExist:
        return Response({
            'error': 'Agendamento não encontrado'
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({
            'error': 'Erro ao confirmar agendamento',
            'detail': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['PATCH'])
@permission_classes([permissions.IsAuthenticated])
def cancelar_agendamento(request, agendamento_id):
    """
    Cancela um agendamento
    """
    try:
        agendamento = Agendamento.objects.get(id=agendamento_id)
        
        # Verificar se o usuário pode cancelar (cliente ou admin/profissional)
        if request.user != agendamento.cliente and request.user.tipo not in ['admin', 'profissional']:
            return Response({
                'error': 'Sem permissão para cancelar este agendamento'
            }, status=status.HTTP_403_FORBIDDEN)
        
        # Aqui você pode adicionar lógica adicional para cancelamento
        # Por exemplo, marcar como cancelado em vez de deletar
        agendamento.delete()
        
        return Response({'message': 'Agendamento cancelado com sucesso'})
    except Agendamento.DoesNotExist:
        return Response({
            'error': 'Agendamento não encontrado'
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({
            'error': 'Erro ao cancelar agendamento',
            'detail': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def horarios_disponiveis(request):
    """
    Busca horários disponíveis para um serviço e data
    """
    try:
        data = request.GET.get('data')
        servico_id = request.GET.get('servico_id')
        profissional_id = request.GET.get('profissional_id')
        
        if not data or not servico_id:
            return Response({
                'error': 'Data e serviço são obrigatórios'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Converter data
        data_obj = datetime.strptime(data, '%Y-%m-%d').date()
        
        # Buscar disponibilidades
        disponibilidades = DisponibilidadeAgenda.objects.filter(
            data=data_obj,
            servico_id=servico_id
        )
        
        if profissional_id:
            disponibilidades = disponibilidades.filter(responsavel_id=profissional_id)
        
        # Buscar agendamentos existentes para excluir horários ocupados
        agendamentos = Agendamento.objects.filter(
            data_hora__date=data_obj,
            servico_id=servico_id
        )
        
        if profissional_id:
            agendamentos = agendamentos.filter(responsavel_id=profissional_id)
        
        horarios_ocupados = [a.data_hora.time() for a in agendamentos]
        
        # Filtrar horários disponíveis
        horarios_disponiveis = []
        for disponibilidade in disponibilidades:
            hora_atual = disponibilidade.hora_inicio
            while hora_atual < disponibilidade.hora_fim:
                if hora_atual not in horarios_ocupados:
                    horarios_disponiveis.append(hora_atual.strftime('%H:%M'))
                hora_atual = (datetime.combine(datetime.today(), hora_atual) + timedelta(minutes=30)).time()
        
        return Response({
            'data': data,
            'servico_id': servico_id,
            'horarios_disponiveis': horarios_disponiveis
        })
        
    except Exception as e:
        return Response({
            'error': 'Erro ao buscar horários disponíveis',
            'detail': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
