from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from . import serializers
from .models import Profile
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.models import User
# Create your views here.





@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer = serializers.RegisterSerializer(data = request.data)
    if serializer.is_valid():
        user = serializer.save()
        token = Token.objects.get(user = user)
        return Response({'data':serializer.data, 'token': token.key})
    return Response({'data': serializer.errors})


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    serializer = serializers.LoginSerializer(data = request.data)
    if serializer.is_valid():
        user = authenticate(username = serializer.data['username'], password = serializer.data['password'])
        token, _ = Token.objects.get_or_create(user= user)
        return Response({'data': serializer.data, 'token': token.key})
    return Response({"data" : serializer.errors})


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def logout(request):
    request.user.auth_token.delete()
    return Response({"data": "logout"})

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def changeInformation(request, id):
    user = User.objects.filter(id = id).first()
    if request.auth.user == user:
        serializer = serializers.UpdateSerializer(user, data= request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'data': serializer.data, 'msg': 'Your information changed successfully'})
        return Response({'msg': serializer.errors})
    return Response({'msg': 'You do not have the rights to change the data'})

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def changePicture(request, id):
    profile = Profile.objects.filter(id = id).first()
    if request.user.profile == profile:
        serializer = serializers.ProfileSerialzier(profile, data= request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'data': serializer.data, 'msg': 'Your information changed successfully'})
        return Response({'msg': serializer.errors})
    return Response({'msg': 'You do not have the rights to change the data'})