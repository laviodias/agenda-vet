from django.shortcuts import render
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.utils import timezone
from datetime import datetime, timedelta
from django.db.models import Count, Sum, Q
from .models import Empresa
from agendamentos.models import Agendamento
from servicos.models import Servico
from usuarios.models import Usuario
from .serializers import EmpresaSerializer

# Create your views here.

class EmpresaViewSet(viewsets.ModelViewSet):
    queryset = Empresa.objects.all()
    serializer_class = EmpresaSerializer

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
