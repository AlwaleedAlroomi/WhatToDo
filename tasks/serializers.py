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
    
    def update(self, instance, validated_data):
        if self.context['user'] == instance.user:
            instance.title = validated_data['title']
            instance.description = validated_data['description']
            instance.due = validated_data['due']
            instance.isCompleted = validated_data['isCompleted']
            instance.save()
            return instance
        raise serializers.ValidationError({"msg": "You do not have the right to edit the data"})