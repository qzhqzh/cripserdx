import os

from django.http import FileResponse
from rest_framework import serializers
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet

from config.celery import run_task
from task.models import Task, Notice
from task.serializers import TaskSerializer, TaskSubmitSerializer, NoticesSerializer


class TaskViewSet(ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def create(self, request, *args, **kwargs):
        self.serializer_class = TaskSubmitSerializer
        super(TaskViewSet, self).create(request, *args, **kwargs)
        return redirect("task")

    @action(['GET'], detail=True)
    def result(self, request, *args, **kwargs):
        """ task detail
        """
        from crisperdx.views import get_common_context

        context = get_common_context(request)
        task = self.get_object()
        context['task'] = task
        context['result'] = task.get_output()
        response = TemplateResponse(self.request, 'detail.html', context)
        return response

    @action(['GET'], detail=True)
    def download_xls(self, request, *args, **kwargs):
        """ task detail
        """
        from crisperdx.views import get_common_context

        context = get_common_context(request)
        task = self.get_object()
        if not os.path.exists(task.output):
            raise serializers.ValidationError('can not find relate file!')

        with open(task.output)as fh:
            save_path = open(task.output, "rb")
            response = FileResponse(save_path)
            response['Content-Type'] = 'application/octet-stream'
            filename = f'attachment; filename={task.id}_result.xls'
            # TODO 设置文件名的包含中文编码方式
            response['Content-Disposition'] = filename.encode('utf-8', 'ISO-8859-1')
            return response


class NoticeViewSet(ModelViewSet):
    queryset = Notice.objects.all()
    serializer_class = NoticesSerializer
