from django.shortcuts import render
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from django.utils import timezone
from datetime import datetime, timedelta
from django.db.models import Sum, Count
from .models import Agendamento
from .serializers import AgendamentoSerializer
from usuarios.models import Usuario
from animais.models import Animal
from servicos.models import Servico
from core.permissions import PermissionChecker, require_permission

class AgendamentoViewSet(viewsets.ModelViewSet):
    queryset = Agendamento.objects.all()
    serializer_class = AgendamentoSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """
        Filtrar agendamentos baseado no role do usuário
        """
        user = self.request.user
        
        # Admins veem todos os agendamentos
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
        
        # Admins podem editar qualquer agendamento
        if PermissionChecker.check_permission(request.user, 'agendamentos', 'update'):
            return super().update(request, *args, **kwargs)
        
        return PermissionChecker.get_permission_response('Você não tem permissão para editar este agendamento')
    
    def destroy(self, request, *args, **kwargs):
        agendamento = self.get_object()
        
        # Cliente pode cancelar apenas seus próprios agendamentos
        if agendamento.cliente == request.user:
            return super().destroy(request, *args, **kwargs)
        
        # Admins podem cancelar qualquer agendamento
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
    Lista todos os agendamentos (admin)
    """
    try:
        agendamentos = Agendamento.objects.select_related(
            'servico', 'animal', 'cliente'
        ).order_by('-data_hora')
        
        serializer = AgendamentoSerializer(agendamentos, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({
            'error': 'Erro ao buscar agendamentos',
            'detail': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def agendamentos_recentes(request):
    """
    Retorna agendamentos recentes para o dashboard
    """
    try:
        agendamentos = Agendamento.objects.select_related(
            'servico', 'animal', 'cliente'
        ).order_by('-data_hora')[:10]
        
        serializer = AgendamentoSerializer(agendamentos, many=True)
        return Response(serializer.data)
        
    except Exception as e:
        return Response({
            'error': 'Erro ao buscar agendamentos recentes',
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
        data['empresa'] = 1  # Usar empresa padrão (ID 1 - AgendaVet)
        
        # Verificar se a data/hora está disponível
        data_hora = datetime.fromisoformat(data['data_hora'].replace('Z', '+00:00'))
        
        # Verificar se já existe agendamento no mesmo horário
        agendamento_existente = Agendamento.objects.filter(
            data_hora=data_hora
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
    Confirma um agendamento (admin)
    """
    try:
        agendamento = Agendamento.objects.get(id=agendamento_id)
        
        # Atualizar status para confirmado
        agendamento.status = 'confirmado'
        agendamento.save()
        
        # Retornar dados do agendamento usando o serializer
        serializer = AgendamentoSerializer(agendamento)
        return Response(serializer.data)
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
        
        # Verificar se o usuário pode cancelar (cliente ou admin)
        if request.user != agendamento.cliente and request.user.tipo != 'admin':
            return Response({
                'error': 'Sem permissão para cancelar este agendamento'
            }, status=status.HTTP_403_FORBIDDEN)
        
        # Marcar como cancelado em vez de deletar
        agendamento.status = 'cancelado'
        agendamento.save()
        
        # Retornar dados do agendamento usando o serializer
        serializer = AgendamentoSerializer(agendamento)
        return Response(serializer.data)
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
            'cliente', 'animal', 'servico'
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
                'data_hora': agendamento.data_hora,
                'observacoes': agendamento.observacoes,
                'status': agendamento.status
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
        
        # Usar empresa com ID 1 fixo
        from core.models import Empresa
        empresa = Empresa.objects.get(id=1)
        
        # Buscar objetos relacionados
        cliente = Usuario.objects.get(id=data['cliente_id'], tipo='cliente')
        animal = Animal.objects.get(id=data['animal_id'])
        servico = Servico.objects.get(id=data['servico_id'])
        
        # Criar agendamento
        agendamento = Agendamento.objects.create(
            empresa=empresa,
            cliente=cliente,
            animal=animal,
            servico=servico,
            data_hora=data['data_hora'],
            observacoes=data.get('observacoes', '')
        )
        
        return Response({
            'id': agendamento.id,
            'message': 'Agendamento criado com sucesso'
        })
    except Empresa.DoesNotExist:
        return Response({'error': 'Empresa não encontrada'}, status=404)
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
        agendamento.status = data.get('status', agendamento.status)
        
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
        
        status = data.get('status', 'confirmado')
        agendamento.status = status
        agendamento.save()
        
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
@permission_classes([permissions.IsAuthenticated])
def horarios_disponiveis(request):
    """
    Busca horários disponíveis para uma data
    """
    try:
        data = request.GET.get('data')
        
        if not data:
            return Response({
                'error': 'Data é obrigatória'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Converter data
        data_obj = datetime.strptime(data, '%Y-%m-%d').date()
        
        # Verificar se é fim de semana
        weekday = data_obj.weekday()
        if weekday == 6:  # Domingo
            return Response([])  # Domingo fechado
        
        # Horários padrão disponíveis
        if weekday == 5:  # Sábado
            horarios_padrao = [
                '08:00', '08:30', '09:00', '09:30', '10:00', '10:30', '11:00', '11:30'
            ]
        else:  # Segunda a Sexta
            horarios_padrao = [
                '08:00', '08:30', '09:00', '09:30', '10:00', '10:30', '11:00', '11:30', 
                '14:00', '14:30', '15:00', '15:30', '16:00', '16:30', '17:00', '17:30'
            ]
        
        # Buscar agendamentos existentes para excluir horários ocupados
        agendamentos = Agendamento.objects.filter(
            data_hora__date=data_obj
        )
        
        # Converter horários ocupados para formato string
        horarios_ocupados = [
            a.data_hora.strftime('%H:%M') for a in agendamentos
        ]
        
        # Filtrar horários disponíveis
        horarios_disponiveis = [
            horario for horario in horarios_padrao 
            if horario not in horarios_ocupados
        ]
        
        return Response(horarios_disponiveis)
        
    except Exception as e:
        return Response({
            'error': 'Erro ao buscar horários disponíveis',
            'detail': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
@require_permission('agendamentos', 'read')
def get_horarios_disponiveis_admin(request):
    """Buscar horários disponíveis para admin"""
    try:
        data = request.GET.get('data')
        
        if not data:
            return Response({
                'error': 'Data é obrigatória'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Converter data
        data_obj = datetime.strptime(data, '%Y-%m-%d').date()
        
        # Verificar se é fim de semana
        weekday = data_obj.weekday()
        if weekday == 6:  # Domingo
            return Response([])  # Domingo fechado
        
        # Horários padrão disponíveis
        if weekday == 5:  # Sábado
            horarios_padrao = [
                '08:00', '08:30', '09:00', '09:30', '10:00', '10:30', '11:00', '11:30'
            ]
        else:  # Segunda a Sexta
            horarios_padrao = [
                '08:00', '08:30', '09:00', '09:30', '10:00', '10:30', '11:00', '11:30', 
                '14:00', '14:30', '15:00', '15:30', '16:00', '16:30', '17:00', '17:30'
            ]
        
        # Buscar agendamentos existentes para excluir horários ocupados
        agendamentos = Agendamento.objects.filter(
            data_hora__date=data_obj
        )
        
        # Converter horários ocupados para formato string
        horarios_ocupados = [
            a.data_hora.strftime('%H:%M') for a in agendamentos
        ]
        
        # Filtrar horários disponíveis
        horarios_disponiveis = [
            horario for horario in horarios_padrao 
            if horario not in horarios_ocupados
        ]
        
        return Response(horarios_disponiveis)
        
    except Exception as e:
        return Response({
            'error': 'Erro ao buscar horários disponíveis',
            'detail': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
