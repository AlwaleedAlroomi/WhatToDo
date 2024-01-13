from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from . import serializers
from .models import Profile
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.models import User
import uuid
from .helpers import send_forget_password_email, send_email_verification_email
# Create your views here.





@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer = serializers.RegisterSerializer(data = request.data)
    if serializer.is_valid():
        user = serializer.save()
        token = Token.objects.get(user = user)
        return Response({'data':serializer.data, 'msg': 'check your inbox to activate your account', 'token': token.key})
    return Response({'data': serializer.errors})


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    serializer = serializers.LoginSerializer(data = request.data)
    if serializer.is_valid():
        user = authenticate(username = serializer.data['username'], password = serializer.data['password'])
        if not user:
            return Response({"error":"Invalid Credentials"})
        profile = Profile.objects.get(user = user)
        if not profile.is_verified:
            return Response({'msg': 'activate your account'})
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


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def forgetPassword(request, id):
    user = User.objects.filter(id = id).first()
    if request.auth.user == user:
        token = str(uuid.uuid4())
        profile = Profile.objects.get(user = user)
        profile.reset_password_token = token
        profile.save()
        send_forget_password_email(email= user.email, token=token)
        return Response({'msg': 'Check your email inbox'})
    return Response({'msg': 'You do not have the rights to change the data'})

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def changePassword(request, id):
    user = User.objects.get(id = id)
    profile = Profile.objects.filter(user = user).first()
    if request.auth.user == user:
        new_password = request.POST.get('password')
        new_password_confirm = request.POST.get('password2')
        if profile.reset_password_token == request.POST.get('token'):
            if new_password == new_password_confirm:
                serializer = serializers.ChangePasswordSerializer(user, request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response({'data': serializer.data, 'msg': 'your password changed'})
                return Response({'data': serializer.errors})
            return Response({'data': 'password are not the same'})
        return Response({'msg':'Check your token and try again later'})
    return Response({'msg': 'You do not have the rights to change the password'})


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def verifyEmail(request, id):
    user = User.objects.get(id = id)
    profile = Profile.objects.filter(user = user).first()
    if request.auth.user == user:
        token = request.POST.get('token')
        if token == profile.email_verification_token:
            serializer = serializers.VerifyEmailSerializer(profile, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"data": serializer.data, 'msg': 'your account activated'})
            return Response({'msg': serializer.errors})
        return Response({'data': 'tokens are not the same'})
    return Response({'msg': 'You do not have the rights to change the data'})
    
        