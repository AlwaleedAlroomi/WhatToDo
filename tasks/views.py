from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from . import serializers
from .models import Task
from rest_framework.permissions import IsAuthenticated
from rest_framework import status


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_tasks(request):
    tasks =Task.objects.filter(user = request.user)
    serializer = serializers.TaskSerializer(tasks, many=True)
    return Response({'data': serializer.data}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_task(request):
    serializer = serializers.TaskSerializer(data=request.data, context={'user':request.user})
    if serializer.is_valid():
        serializer.save()
        return Response({"data": serializer.data})
    return Response({'data':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def edit_task(request, id):
    task = Task.objects.filter(id=id).first()
    serializer = serializers.TaskSerializer(instance=task, data=request.data, context={'user': request.user})
    if serializer.is_valid():
        serializer.save()
        return Response({"data": serializer.data})
    return Response({'data':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_task(request, id):
    task = Task.objects.filter(id=id).first()
    if request.user == task.user:
        task.delete()
        return Response({"msg": "task deleted"})
    return Response({'msg':"You do not have the right to delete the task"}, status=status.HTTP_403_FORBIDDEN)