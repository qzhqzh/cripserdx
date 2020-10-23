""" description """
from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    submitter = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), default=serializers.CurrentUserDefault())

    class Meta:
        model = Task
        fields = ['status', 'cmd', 'rc', 'msg', 'submitter', 'started_at', 'finished_at']

class PcrTaskSubmitSerializer(TaskSerializer):
    method = serializers.CharField(default='pcr')
    dna_sequence = serializers.CharField(write_only=True)
    genome = serializers.CharField(write_only=True)
    length_of_protospacer = serializers.CharField(write_only=True)
    pam_sequence = serializers.CharField(write_only=True)
    dna_direction = serializers.CharField(write_only=True)
    location = serializers.CharField(write_only=True)
    gc_content = serializers.CharField(write_only=True)
    mismatches_number = serializers.CharField(write_only=True)

    class Meta:
        model = Task
        fields = TaskSerializer.Meta.fields + ['method', 'dna_sequence', 'genome', 'length_of_protospacer', 'pam_sequence',
                  'dna_direction', 'location', 'gc_content', 'mismatches_number']

    def create(self, validated_data):
        print(validated_data)
        return Task.objects.first()
