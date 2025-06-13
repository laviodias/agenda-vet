from django.shortcuts import render
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import Animal
from .serializers import AnimalSerializer, AnimalDetailSerializer

# Create your views here.

class AnimalViewSet(viewsets.ModelViewSet):
    queryset = Animal.objects.all()
    serializer_class = AnimalSerializer

@api_view(['GET'])
def listar_pets(request):
    """
    Lista pets do usuário logado
    """
    try:
        pets = Animal.objects.filter(dono=request.user)
        serializer = AnimalSerializer(pets, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({
            'error': 'Erro ao buscar pets',
            'detail': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def criar_pet(request):
    """
    Cria um novo pet para o usuário logado
    """
    try:
        data = request.data.copy()
        data['dono'] = request.user.id
        
        # Buscar empresa padrão
        from core.models import Empresa
        empresa_padrao, created = Empresa.objects.get_or_create(
            nome='Clínica Veterinária Padrão',
            defaults={
                'cnpj': '00.000.000/0001-00',
                'endereco': 'Endereço padrão',
                'telefone': '(11) 99999-9999'
            }
        )
        data['empresa'] = empresa_padrao.id
        
        serializer = AnimalSerializer(data=data)
        if serializer.is_valid():
            pet = serializer.save()
            return Response(AnimalSerializer(pet).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    except Exception as e:
        return Response({
            'error': 'Erro ao criar pet',
            'detail': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PUT'])
def atualizar_pet(request, pet_id):
    """
    Atualiza um pet do usuário logado
    """
    try:
        pet = Animal.objects.get(id=pet_id, dono=request.user)
        serializer = AnimalSerializer(pet, data=request.data, partial=True)
        if serializer.is_valid():
            pet = serializer.save()
            return Response(AnimalSerializer(pet).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    except Animal.DoesNotExist:
        return Response({
            'error': 'Pet não encontrado'
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({
            'error': 'Erro ao atualizar pet',
            'detail': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['DELETE'])
def deletar_pet(request, pet_id):
    """
    Deleta um pet do usuário logado
    """
    try:
        pet = Animal.objects.get(id=pet_id, dono=request.user)
        pet.delete()
        return Response({'message': 'Pet deletado com sucesso'})
        
    except Animal.DoesNotExist:
        return Response({
            'error': 'Pet não encontrado'
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({
            'error': 'Erro ao deletar pet',
            'detail': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
