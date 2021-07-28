from rest_framework import serializers

from .models import UserMessageThread, UserMessage
from tasks.serializers import TaskSerializer
from users.serializers import CustomUserSerializer


class MessageThreadSerializer(serializers.HyperlinkedModelSerializer):
    created_by = CustomUserSerializer(read_only=True)
    recipient = CustomUserSerializer(read_only=True)
    job = TaskSerializer(read_only=True)

    class Meta:
        model = UserMessageThread
        fields = ['id', 'created_by', 'recipient', 'job', 'created_on', ]


class MessageSerializer(serializers.HyperlinkedModelSerializer):
    sender = CustomUserSerializer(read_only=True)
    recipient = CustomUserSerializer(read_only=True)

    class Meta:
        model = UserMessage
        fields = ['id', 'sender', 'recipient', 'message_body', 'timestamp', 'status', ]
