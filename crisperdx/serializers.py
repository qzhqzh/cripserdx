""" description """
from rest_framework import serializers

from crisperdx.models import Setting


class SettingSerializer(serializers.ModelSerializer):
    """系统设置的序列化"""
    class Meta:
        model = Setting
        fields = '__all__'
