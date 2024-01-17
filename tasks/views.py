from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from . import serializers
from .models import Task
from rest_framework.permissions import IsAuthenticated


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_tasks(request):
    tasks =Task.objects.filter(user = request.user)
    serializer = serializers.TaskSerializer(tasks, many=True)
    return Response({'data': serializer.data})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_task(request):
    serializer = serializers.TaskSerializer(data=request.data, context={'user':request.user})
    if serializer.is_valid():
        serializer.save()
        return Response({"data": serializer.data})
    return Response({'data':serializer.errors})