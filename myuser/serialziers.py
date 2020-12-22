""" description """

from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """ User info serializer
    For user to update his or her information
    """

    task_info = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('task_info',)

    def get_task_info(self, obj):
        tasks = obj.tasks
        task_info = {
            'fail': tasks.filter(status=-1).count(),
            'waiting': tasks.filter(status=0).count(),
            'running': tasks.filter(status=1).count(),
            'success': tasks.filter(status=2).count(),
        }
        return task_info
