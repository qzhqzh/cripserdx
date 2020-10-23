from django.shortcuts import redirect
from rest_framework.viewsets import ModelViewSet

from task.models import Task
from task.serializers import TaskSerializer, PcrTaskSubmitSerializer


class TaskViewSet(ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def get_serializer_class(self):
        if self.request.data.get('method') == 'pcr' and self.request.method == 'POST':
            return PcrTaskSubmitSerializer
        return TaskSerializer

    def create(self, request, *args, **kwargs):
        super(TaskViewSet, self).create(request, *args, **kwargs)
        return redirect("task")