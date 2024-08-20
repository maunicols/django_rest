from api.serializer import UserSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

# Create your views here.
@api_view(['POST'])
def login(request):
    user= get_object_or_404(User, username=request.data['username'])
    if not user.check_password(request.data['password']):
        return Response({"error": "Invalid password"}, status=status.HTTP_400_BAD_REQUEST)
    token, created = Token.objects.get_or_create(user=user)
    serialized= UserSerializer(instance=user)
    return Response({"token": token.key, "user": serialized.data}, status=status.HTTP_202_ACCEPTED)

@api_view(['POST'])
def register(request):
    serialized = UserSerializer(data= request.data)
    if serialized.is_valid():
        serialized.save()
        user= User.objects.get(username=serialized.data['username'])
        user.set_password(serialized.data['password'])
        user.save()
        token = Token.objects.create(user=user)
        return Response({'token': token.key,
                        'user': serialized.data
                        }, status=status.HTTP_201_CREATED)
    return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def profile(request):
    
    print(request.headers)
    return Response({f'Token authentication for {request.user.username} is valid'}, status=status.HTTP_200_OK)


@api_view(['GET'])
def logout(request):
    return Response({})