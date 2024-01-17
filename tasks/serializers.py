from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
        extra_kwargs = {
            'user':{'read_only':True}
        }


    def create(self, validated_data):
        validated_data['user'] = self.context['user']
        task = Task.objects.create(
            user = validated_data['user'],
            title = validated_data['title'],
            description = validated_data['description'],
        )
        return task
    