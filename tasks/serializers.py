from rest_framework import serializers
from .models import Task
from django.db import transaction
from django.db.models import F, Max
from datetime import datetime

class TaskListCreateSerializer(serializers.Serializer):
    id = serializers.UUIDField(required=False)
    title = serializers.CharField(required=True)
    description = serializers.CharField(required=False, default='')
    is_checklist = serializers.BooleanField(required=False, default=False)
    is_pinned = serializers.BooleanField(required=False, default=False)
    due_date = serializers.DateField(required=False, default=None)
    priority = serializers.ChoiceField(required=False, choices=Task.Priority.choices, default=Task.Priority.MEDIUM)
    sequence = serializers.IntegerField(required=False, default=0, min_value=0)
    status = serializers.ChoiceField(required=False, choices=Task.Status.choices, default=Task.Status.PENDING)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def validate_due_date(self, value):
        if value < datetime.now().date():
            raise serializers.ValidationError("Due date cannot be in the past")
        return value
    
    def validate_priority(self, value):
        if value not in Task.Priority.values:
            raise serializers.ValidationError("Invalid priority")
        return value
    
    def validate_status(self, value):
        if value not in Task.Status.values:
            raise serializers.ValidationError("Invalid status")
        return value

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        validated_data['sequence'] = Task.objects.filter(user=validated_data['user']).count() + 1
        return Task.objects.create(**validated_data)

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'is_checklist', 'is_pinned', 'due_date', 'priority', 'sequence', 'status']
        ordering = ['sequence']
    
    def update(self, instance, validated_data):
        validated_data['user'] = instance.user
        return super().update(instance, validated_data)
    
    def validate_due_date(self, value):
        if value < datetime.now().date():
            raise serializers.ValidationError("Due date cannot be in the past")
        return value
    
    def validate_priority(self, value):
        if value not in Task.Priority.values:
            raise serializers.ValidationError("Invalid priority")
        return value
    
    def validate_status(self, value):
        if value not in Task.Status.values:
            raise serializers.ValidationError("Invalid status")
        return value

class TaskSequenceSerializer(serializers.Serializer):
    id = serializers.UUIDField(required=True)
    sequence = serializers.IntegerField(required=True, min_value=0)

    def validate(self, attrs):
        # ensure task exists and belongs to user
        request = self.context.get("request")
        if request is None or not hasattr(request, "user"):
            raise serializers.ValidationError("Request user is required in serializer context.")

        task_id = attrs.get("id")
        task = Task.objects.filter(id=task_id, user=request.user).first()
        if not task:
            raise serializers.ValidationError({"id": "Task not found or does not belong to the user."})

        attrs["_task_instance"] = task  # attach instance for save()
        return attrs

    def save(self, **kwargs):
        """
        Perform the reorder and return the moved Task instance.
        """
        validated = self.validated_data
        task: Task = validated["_task_instance"]
        user = self.context["request"].user
        new_seq = validated["sequence"]

        # compute current max sequence for this user (None -> -1)
        max_seq = Task.objects.filter(user=user).aggregate(max_seq=Max("sequence"))["max_seq"]
        if max_seq is None:
            max_seq = 0
        # clamp new_seq into [0, max_seq] so moving beyond end appends to end
        if new_seq > max_seq:
            new_seq = max_seq

        old_seq = task.sequence

        # nothing to do
        if new_seq == old_seq:
            return task

        with transaction.atomic():
            if new_seq < old_seq:
                # moving up (toward 0): shift tasks in [new_seq, old_seq-1] right by 1
                Task.objects.filter(
                    user=user,
                    sequence__gte=new_seq,
                    sequence__lt=old_seq,
                ).update(sequence=F("sequence") + 1)
            else:
                # moving down (toward end): shift tasks in [old_seq+1, new_seq] left by 1
                Task.objects.filter(
                    user=user,
                    sequence__gt=old_seq,
                    sequence__lte=new_seq,
                ).update(sequence=F("sequence") - 1)

            # finally set the task's new sequence
            task.sequence = new_seq
            task.save(update_fields=["sequence"])

        return task