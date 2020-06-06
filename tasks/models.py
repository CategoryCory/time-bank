from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model


class Offer(models.Model):
    AVAILABLE = 'AVAILABLE'
    IN_PROGRESS = 'IN_PROGRESS'
    COMPLETED = 'COMPLETED'
    STATUS_CHOICES = [
        (AVAILABLE, 'Available'),
        (IN_PROGRESS, 'In Progress'),
        (COMPLETED, 'Completed'),
    ]

    title = models.CharField(max_length=150)
    description = models.TextField()
    expires = models.DateField(default=timezone.now, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=AVAILABLE)
    created_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    categories = models.ManyToManyField('categories.Category', related_name='offers')

    def __str__(self):
        return self.title


class Request(models.Model):
    AVAILABLE = 'AVAILABLE'
    IN_PROGRESS = 'IN_PROGRESS'
    COMPLETED = 'COMPLETED'
    STATUS_CHOICES = [
        (AVAILABLE, 'Available'),
        (IN_PROGRESS, 'In Progress'),
        (COMPLETED, 'Completed'),
    ]

    title = models.CharField(max_length=150)
    description = models.TextField()
    expires = models.DateField(default=timezone.now, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=AVAILABLE)
    created_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    categories = models.ManyToManyField('categories.Category', related_name='requests')

    def __str__(self):
        return self.title
