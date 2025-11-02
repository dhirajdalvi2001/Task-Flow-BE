from django.shortcuts import render
from .models import Task
from .serializers import TaskListCreateSerializer, TaskSerializer, TaskSequenceSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
import uuid
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.db.models import F

class TaskListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TaskListCreateSerializer
    queryset = Task.objects.all()

    def get(self, request, *args, **kwargs):
        tasks = Task.objects.filter(user=request.user)
        serializer = TaskListCreateSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = TaskListCreateSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TaskDetailsUpdateDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id: uuid.UUID):
        try:
            task = Task.objects.get(id=id, user=request.user)
        except Task.DoesNotExist:
            return Response({"message": "Task not found"}, status=status.HTTP_404_NOT_FOUND)
        task = Task.objects.get(id=id, user=request.user)
        serializer = TaskSerializer(task)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        task = Task.objects.get(id=kwargs['id'])
        serializer = TaskSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id: uuid.UUID):
        # ensure existence & ownership
        task = get_object_or_404(Task, id=id, user=request.user)
        deleted_seq = task.sequence

        with transaction.atomic():
            task.delete()
            # shift tasks after deleted_seq left by 1
            Task.objects.filter(user=request.user, sequence__gt=deleted_seq).update(sequence=F('sequence') - 1)

        return Response({"message": "Task deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class TaskSequenceView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = TaskSequenceSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        task = serializer.save()
        return Response(
            {
                "message": "Task reordered successfully",
                "task": TaskSerializer(task).data
            },
            status=status.HTTP_200_OK
        )