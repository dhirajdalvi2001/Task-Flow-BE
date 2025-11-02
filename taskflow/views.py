from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from tasks.models import Task
from django.utils import timezone
from datetime import timedelta
from taskflow.models import User

class ChartView(APIView):
    def get(self, request):
        is_superuser = request.user.is_superuser

        total_tasks = Task.objects.filter(user=request.user).count()
        pending_tasks = Task.objects.filter(user=request.user, status=Task.Status.PENDING).count()
        in_progress_tasks = Task.objects.filter(user=request.user, status=Task.Status.IN_PROGRESS).count()
        completed_tasks = Task.objects.filter(user=request.user, status=Task.Status.COMPLETED).count()
        cancelled_tasks = Task.objects.filter(user=request.user, status=Task.Status.CANCELLED).count()

        tasks_due_in_three_days = Task.objects.filter(user=request.user, due_date__lte=timezone.now() + timedelta(days=3)).count()
        tasks_overdue = Task.objects.filter(user=request.user, status=Task.Status.PENDING, due_date__lt=timezone.now()).count()

        data = {
            "total_tasks": total_tasks,
            "pending_tasks": pending_tasks,
            "in_progress_tasks": in_progress_tasks,
            "completed_tasks": completed_tasks,
            "cancelled_tasks": cancelled_tasks,
            "tasks_due_in_three_days": tasks_due_in_three_days,
            "tasks_overdue": tasks_overdue,
        }

        if is_superuser:
            data["total_users"] = User.objects.count()
            data["total_active_users"] = User.objects.filter(is_active=True).count()
            data["total_inactive_users"] = User.objects.filter(is_active=False).count()

        return Response(data, status=status.HTTP_200_OK)