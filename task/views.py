from rest_framework.viewsets import ModelViewSet

from task.models import Task
from task.serializers import TaskSerializer


class TaskViewSet(ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
