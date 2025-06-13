from django.shortcuts import render
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import Servico
from .serializers import ServicoSerializer

# Create your views here.

class ServicoViewSet(viewsets.ModelViewSet):
    queryset = Servico.objects.all()
    serializer_class = ServicoSerializer

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
