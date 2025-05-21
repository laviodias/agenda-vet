from django.shortcuts import render
from rest_framework import viewsets
from .models import Servico
from .serializers import ServicoSerializer

# Create your views here.

class ServicoViewSet(viewsets.ModelViewSet):
    queryset = Servico.objects.all()
    serializer_class = ServicoSerializer
