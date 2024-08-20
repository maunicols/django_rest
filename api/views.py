from api.serializer import UserSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework import status

# Create your views here.
@api_view(['POST'])
def login(request):
    return Response({})
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

@api_view(['POST'])
def profile(request):
    return Response({})
@api_view(['POST'])
def logout(request):
    return Response({})