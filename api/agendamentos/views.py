from django.shortcuts import render
from rest_framework import viewsets
from .models import DisponibilidadeAgenda, Agendamento
from .serializers import DisponibilidadeAgendaSerializer, AgendamentoSerializer

# Create your views here.

class DisponibilidadeAgendaViewSet(viewsets.ModelViewSet):
    queryset = DisponibilidadeAgenda.objects.all()
    serializer_class = DisponibilidadeAgendaSerializer

class AgendamentoViewSet(viewsets.ModelViewSet):
    queryset = Agendamento.objects.all()
    serializer_class = AgendamentoSerializer
