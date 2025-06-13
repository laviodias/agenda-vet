from django.shortcuts import render
from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .serializers import LoginSerializer, RegistroClienteSerializer, UsuarioSerializer
from .models import Usuario


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
