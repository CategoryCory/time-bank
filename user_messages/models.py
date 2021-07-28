from django.db import models
from django.contrib.auth import get_user_model

from tasks.models import Task

CustomUser = get_user_model()


class UserMessageThread(models.Model):
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='message_thread_created_by')
    recipient = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='message_thread_recipients')
    job = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='message_thread_jobs', blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.created_by}: Message thread {self.id}'
    
    class Meta:
        verbose_name = 'User Message Thread'
        verbose_name_plural = 'User Message Threads'


class UserMessage(models.Model):
    READ = 'READ'
    UNREAD = 'UNREAD'
    STATUS_CHOICES = [
        (READ, 'Read'),
        (UNREAD, 'Unread'),
    ]

    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='message_senders')
    recipient = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='message_recipients')
    message_body = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=UNREAD)
    thread = models.ForeignKey(UserMessageThread, on_delete=models.CASCADE, related_name='user_messages')

    def __str__(self) -> str:
        return f'{self.sender}: Message {self.id}'
    
    class Meta:
        verbose_name = 'User Message'
        verbose_name_plural = 'User Messages'
