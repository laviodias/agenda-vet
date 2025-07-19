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
from animais.models import Animal

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


# ===== VIEWS PARA ADMIN =====

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
@require_permission('agendamentos', 'read')
def get_agendamentos_admin(request):
    """Listar todos os agendamentos para admin"""
    try:
        agendamentos = Agendamento.objects.select_related(
            'cliente', 'animal', 'servico', 'responsavel'
        ).order_by('-data_hora')
        
        data = []
        for agendamento in agendamentos:
            data.append({
                'id': agendamento.id,
                'cliente_id': agendamento.cliente.id,
                'cliente_nome': agendamento.cliente.nome,
                'animal_id': agendamento.animal.id,
                'animal_nome': agendamento.animal.nome,
                'servico_id': agendamento.servico.id,
                'servico_nome': agendamento.servico.nome,
                'responsavel_id': agendamento.responsavel.id if agendamento.responsavel else None,
                'responsavel_nome': agendamento.responsavel.nome if agendamento.responsavel else None,
                'data_hora': agendamento.data_hora,
                'observacoes': agendamento.observacoes,
                'status': 'confirmado'  # Status padrão
            })
        return Response(data)
    except Exception as e:
        return Response({'error': str(e)}, status=500)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
@require_permission('agendamentos', 'create')
def create_agendamento_admin(request):
    """Criar novo agendamento para admin"""
    try:
        data = request.data
        
        # Buscar objetos relacionados
        cliente = Usuario.objects.get(id=data['cliente_id'], tipo='cliente')
        animal = Animal.objects.get(id=data['animal_id'])
        servico = Servico.objects.get(id=data['servico_id'])
        responsavel = None
        if data.get('responsavel_id'):
            responsavel = Usuario.objects.get(id=data['responsavel_id'], tipo='profissional')
        
        # Criar agendamento
        agendamento = Agendamento.objects.create(
            cliente=cliente,
            animal=animal,
            servico=servico,
            responsavel=responsavel,
            data_hora=data['data_hora'],
            observacoes=data.get('observacoes', '')
        )
        
        return Response({
            'id': agendamento.id,
            'message': 'Agendamento criado com sucesso'
        })
    except Usuario.DoesNotExist:
        return Response({'error': 'Usuário não encontrado'}, status=404)
    except Animal.DoesNotExist:
        return Response({'error': 'Animal não encontrado'}, status=404)
    except Servico.DoesNotExist:
        return Response({'error': 'Serviço não encontrado'}, status=404)
    except Exception as e:
        return Response({'error': str(e)}, status=400)


@api_view(['PUT'])
@permission_classes([permissions.IsAuthenticated])
@require_permission('agendamentos', 'update')
def update_agendamento_admin(request, agendamento_id):
    """Atualizar agendamento para admin"""
    try:
        agendamento = Agendamento.objects.get(id=agendamento_id)
        data = request.data
        
        # Atualizar campos básicos
        agendamento.data_hora = data.get('data_hora', agendamento.data_hora)
        agendamento.observacoes = data.get('observacoes', agendamento.observacoes)
        
        # Atualizar relacionamentos se fornecidos
        if 'cliente_id' in data:
            cliente = Usuario.objects.get(id=data['cliente_id'], tipo='cliente')
            agendamento.cliente = cliente
        
        if 'animal_id' in data:
            animal = Animal.objects.get(id=data['animal_id'])
            agendamento.animal = animal
        
        if 'servico_id' in data:
            servico = Servico.objects.get(id=data['servico_id'])
            agendamento.servico = servico
        
        if 'responsavel_id' in data:
            responsavel = None
            if data['responsavel_id']:
                responsavel = Usuario.objects.get(id=data['responsavel_id'], tipo='profissional')
            agendamento.responsavel = responsavel
        
        agendamento.save()
        
        return Response({'message': 'Agendamento atualizado com sucesso'})
    except Agendamento.DoesNotExist:
        return Response({'error': 'Agendamento não encontrado'}, status=404)
    except Usuario.DoesNotExist:
        return Response({'error': 'Usuário não encontrado'}, status=404)
    except Animal.DoesNotExist:
        return Response({'error': 'Animal não encontrado'}, status=404)
    except Servico.DoesNotExist:
        return Response({'error': 'Serviço não encontrado'}, status=404)
    except Exception as e:
        return Response({'error': str(e)}, status=400)


@api_view(['PATCH'])
@permission_classes([permissions.IsAuthenticated])
@require_permission('agendamentos', 'update')
def update_agendamento_status_admin(request, agendamento_id):
    """Atualizar status do agendamento para admin"""
    try:
        agendamento = Agendamento.objects.get(id=agendamento_id)
        data = request.data
        
        # Por enquanto, vamos apenas simular o status
        # Em um sistema real, você teria um campo status no modelo
        status = data.get('status', 'confirmado')
        
        return Response({
            'message': f'Status do agendamento atualizado para {status}',
            'status': status
        })
    except Agendamento.DoesNotExist:
        return Response({'error': 'Agendamento não encontrado'}, status=404)
    except Exception as e:
        return Response({'error': str(e)}, status=400)


@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticated])
@require_permission('agendamentos', 'delete')
def delete_agendamento_admin(request, agendamento_id):
    """Excluir agendamento para admin"""
    try:
        agendamento = Agendamento.objects.get(id=agendamento_id)
        agendamento.delete()
        
        return Response({'message': 'Agendamento excluído com sucesso'})
    except Agendamento.DoesNotExist:
        return Response({'error': 'Agendamento não encontrado'}, status=404)
    except Exception as e:
        return Response({'error': str(e)}, status=400)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
@require_permission('agendamentos', 'read')
def get_agendamento_stats_admin(request):
    """Buscar estatísticas de agendamentos para admin"""
    try:
        total_agendamentos = Agendamento.objects.count()
        
        # Agendamentos de hoje
        hoje = timezone.now()
        hoje_inicio = hoje.replace(hour=0, minute=0, second=0, microsecond=0)
        hoje_fim = hoje.replace(hour=23, minute=59, second=59, microsecond=999999)
        agendamentos_hoje = Agendamento.objects.filter(
            data_hora__gte=hoje_inicio,
            data_hora__lte=hoje_fim
        ).count()
        
        # Agendamentos da semana
        inicio_semana = hoje - timedelta(days=hoje.weekday())
        fim_semana = inicio_semana + timedelta(days=6)
        agendamentos_semana = Agendamento.objects.filter(
            data_hora__gte=inicio_semana,
            data_hora__lte=fim_semana
        ).count()
        
        # Agendamentos do mês
        inicio_mes = hoje.replace(day=1)
        fim_mes = (inicio_mes + timedelta(days=32)).replace(day=1) - timedelta(days=1)
        agendamentos_mes = Agendamento.objects.filter(
            data_hora__gte=inicio_mes,
            data_hora__lte=fim_mes
        ).count()
        
        return Response({
            'totalAgendamentos': total_agendamentos,
            'agendamentosHoje': agendamentos_hoje,
            'agendamentosSemana': agendamentos_semana,
            'agendamentosMes': agendamentos_mes
        })
    except Exception as e:
        return Response({'error': str(e)}, status=400)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
@require_permission('usuarios', 'read')
def get_responsaveis_admin(request):
    """Buscar responsáveis (profissionais) para admin"""
    try:
        responsaveis = Usuario.objects.filter(tipo='profissional').order_by('nome')
        data = []
        for responsavel in responsaveis:
            data.append({
                'id': responsavel.id,
                'nome': responsavel.nome,
                'email': responsavel.email,
                'especialidade': responsavel.especialidade
            })
        return Response(data)
    except Exception as e:
        return Response({'error': str(e)}, status=500)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
@require_permission('servicos', 'read')
def get_servicos_admin(request):
    """Buscar serviços para admin"""
    try:
        servicos = Servico.objects.all().order_by('nome')
        data = []
        for servico in servicos:
            data.append({
                'id': servico.id,
                'nome': servico.nome,
                'descricao': servico.descricao,
                'duracao': servico.duracao,
                'preco': servico.preco
            })
        return Response(data)
    except Exception as e:
        return Response({'error': str(e)}, status=500)

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
