from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from .models import Profile
from django.contrib.auth import authenticate

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'id']
        extra_kwargs = {
            'id':{'read_only':True},
            'password':{'write_only':True}
        }

    def validate(self, data):
        if User.objects.filter(email=data['email']).exists() or User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError("Email is already exists")
        return data

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
        )
        Token.objects.create(user=user)
        return user
    
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
  
        if username and password:
            user = authenticate(username = username, password = password)
            if not user:
                raise serializers.ValidationError({'msg': 'check your username or password and try again'})

        
        profile = Profile.objects.get(user = user)
        if not profile.is_verified:
            raise serializers.ValidationError({'msg': 'activate your account'})
        
        token, _= Token.objects.get_or_create(user= user.id)
        del data['password']
        data['token'] = token.key
        data['id'] = user.id
        return data

class UpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']

    def validate(self, data):
        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError("Username is already exists")
        return data
    
    def update(self, instance, validated_data):
        instance.username = validated_data['username']
        instance.save()
        return instance
    
class ProfileSerialzier(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['profile_picture']

    
    def update(self, instance, validated_data):
        instance.profile_picture = validated_data['profile_picture']
        instance.save()
        return instance
    

class ChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(required=True)
    token = serializers.CharField(write_only=True)

    def validate(self, data):
        if self.context['user_token'] != data['token']:
            raise serializers.ValidationError("Check the token and try again")
        return data
    

    def update(self, instance, validated_data):
        instance.set_password(validated_data['password'])
        instance.save()
        return instance
    
class VerifyEmailSerializer(serializers.Serializer):
    token = serializers.CharField(write_only=True)

    def validate(self, data):
        if self.context['user_token'] != data['token']:
            raise serializers.ValidationError("Check the token and try again")
        return data
    
    def update(self, instance, validated_data):
        instance.is_verified = True
        instance.save()
        return instance