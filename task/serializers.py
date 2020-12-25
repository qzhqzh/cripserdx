""" description """
import os

from django.contrib.auth.models import User
from rest_framework import serializers

from config.celery import run_task
from crisperdx.models import Setting
from .models import Task, Notice


class TaskSerializer(serializers.ModelSerializer):
    submitter = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), default=serializers.CurrentUserDefault())

    class Meta:
        model = Task
        fields = ['status', 'cmd', 'rc', 'submitter', 'started_at', 'finished_at']


class TaskSubmitSerializer(TaskSerializer):
    fasta_seq = serializers.CharField(max_length=10240, write_only=True)
    pam_seq = serializers.CharField(max_length=128, write_only=True)

    class Meta:
        model = Task
        fields = TaskSerializer.Meta.fields + ['fasta_seq', 'pam_seq']


    def _get_default_setting(self):
        """获取任务运行参数"""
        try:
            home_path = Setting.objects.get(key='CRISPR-offinder-home-path').value
        except:
            raise Exception('Please setting [CRISPR-offinder-home-path]')
        try:
            script = Setting.objects.get(key='CRISPR-offinder-script').value
        except:
            raise Exception('Please setting [CRISPR-offinder-script]')
        try:
            interpreter = Setting.objects.get(key='interpreter').value
        except:
            raise Exception('Please setting [interpreter]')
        try:
            output = Setting.objects.get(key='output').value
        except:
            raise Exception('Please setting [output]')
        return home_path, script, interpreter, output

    def create(self, validated_data):
        fasta_seq = validated_data.pop('fasta_seq')
        pam_seq = validated_data.pop('pam_seq')
        home_path, script, interpreter, output = self._get_default_setting()

        t = super(TaskSubmitSerializer, self).create(validated_data)

        input_dir = os.path.join(output, str(t.id))
        input_file = os.path.join(input_dir, 'input.fa')
        os.makedirs(input_dir, exist_ok=True)
        with open(input_file, 'w')as fh:
            fh.write(fasta_seq)

        cmd = f"cd {home_path}; {interpreter} {script} -input {input_file} -pamseq {pam_seq} -output {input_dir}"
        t.cmd = cmd
        t.save()
        #cid = run_task.apply_async(args=(t,))
        print('start submit')
        cid = run_task.delay(t)
        t.cid = cid
        t.save()
        print(t.cid)
        return t


class NoticesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Notice
        fields = ['id', 'model', 'model_id', 'model_method', 'status', 'started_at', 'finished_at', 'cid']
