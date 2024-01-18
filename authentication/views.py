from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from . import serializers
from .models import Profile
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.models import User
import uuid
from .helpers import send_forget_password_email
from rest_framework import status
# Create your views here.


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer = serializers.RegisterSerializer(data = request.data)
    if serializer.is_valid():
        user = serializer.save()
        data = serializer.data
        data['token'] = Token.objects.get(user = user).key
        return Response({'data':data, 'msg': 'check your inbox to activate your account'})
    return Response({'data': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    serializer = serializers.LoginSerializer(data = request.data)
    if serializer.is_valid():
        print(serializer.validated_data)
        return Response({'data': serializer.validated_data})
    return Response({"data" : serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


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
        return Response({'msg': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    return Response({'msg': 'You do not have the rights to change the data'}, status=status.HTTP_403_FORBIDDEN)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def changePicture(request, id):
    profile = Profile.objects.filter(id = id).first()
    if request.user.profile == profile:
        serializer = serializers.ProfileSerialzier(profile, data= request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'data': serializer.data, 'msg': 'Your information changed successfully'})
        return Response({'msg': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    return Response({'msg': 'You do not have the rights to change the data'}, status=status.HTTP_403_FORBIDDEN)


@api_view(['POST'])
@permission_classes([AllowAny])
def forgetPassword(request):
    user = User.objects.filter(email = request.data['email']).first()
    token = str(uuid.uuid4())
    profile = Profile.objects.get(user = user)
    profile.reset_password_token = token
    profile.save()
    send_forget_password_email(email= user.email, token=token)
    return Response({'msg': 'Check your email inbox'})


@api_view(['PUT'])
@permission_classes([AllowAny])
def changePassword(request):
    user = User.objects.get(email = request.data['email'])
    profile = Profile.objects.filter(user = user).first()
    if request.POST.get('password') == request.POST.get('password2'):
        serializer = serializers.ChangePasswordSerializer(user, request.data, context={'user_token': profile.reset_password_token})
        if serializer.is_valid():
            serializer.save()
            return Response({'data': serializer.data, 'msg': 'your password changed'})
        return Response({'data': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    return Response({'data': 'password are not the same'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def verifyEmail(request, id):
    user = User.objects.get(id = id)
    profile = Profile.objects.filter(user = user).first()
    if request.auth.user == user:
        serializer = serializers.VerifyEmailSerializer(profile, data=request.data, partial=True, context={'user_token':profile.email_verification_token})
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'your account activated'})
        return Response({'msg': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    return Response({'msg': 'You do not have the rights to change the data'}, status=status.HTTP_403_FORBIDDEN)
    
        