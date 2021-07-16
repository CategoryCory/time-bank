from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.urls import reverse


class TaskCategory(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    description = models.TextField()
    parent_category = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='subcategory'
    )

    class Meta:
        verbose_name = 'Task Category'
        verbose_name_plural = 'Task Categories'

    def __str__(self):
        return self.title


class Task(models.Model):
    ONE_TIME = 'ONE_TIME'
    DAILY = 'DAILY'
    WEEKLY = 'WEEKLY'
    BIWEEKLY = 'BIWEEKLY'
    MONTHLY = 'MONTHLY'
    AS_NEEDED = 'AS_NEEDED'
    FREQUENCY_CHOICES = [
        (ONE_TIME, 'One Time'),
        (DAILY, 'Daily'),
        (WEEKLY, 'Weekly'),
        (BIWEEKLY, 'Biweekly'),
        (MONTHLY, 'Monthly'),
        (AS_NEEDED, 'As Needed'),
    ]

    AVAILABLE = 'AVAILABLE'
    UNAVAILABLE = 'UNAVAILABLE'
    COMPLETED = 'COMPLETED'
    DELETED = 'DELETED'
    STATUS_CHOICES = [
        (AVAILABLE, 'Available'),
        (UNAVAILABLE, 'Unavailable'),
        (COMPLETED, 'Completed'),
        (DELETED, 'Deleted'),
    ]

    title = models.CharField(max_length=150)
    description = models.TextField()
    expires_on = models.DateField(default=timezone.now, null=True)
    frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=AVAILABLE)
    categories = models.ManyToManyField(TaskCategory)
    created_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('tasks:task_detail', args=[str(self.id)])

    def soft_delete(self):
        self.status = 'DELETED'
        self.save()

    class Meta:
        indexes = [
            models.Index(fields=['title', ]),
            models.Index(fields=['status', ]),
        ]


class TaskAvailability(models.Model):
    SUNDAY = 'SUNDAY'
    MONDAY = 'MONDAY'
    TUESDAY = 'TUESDAY'
    WEDNESDAY = 'WEDNESDAY'
    THURSDAY = 'THURSDAY'
    FRIDAY = 'FRIDAY'
    SATURDAY = 'SATURDAY'
    MORNING = 'MORNING'
    AFTERNOON = 'AFTERNOON'
    EVENING = 'EVENING'

    DAY_CHOICES = [
        (SUNDAY, 'Sunday'),
        (MONDAY, 'Monday'),
        (TUESDAY, 'Tuesday'),
        (WEDNESDAY, 'Wednesday'),
        (THURSDAY, 'Thursday'),
        (FRIDAY, 'Friday'),
        (SATURDAY, 'Saturday'),
    ]

    TIME_CHOICES = [
        (MORNING, 'Morning'),
        (AFTERNOON, 'Afternoon'),
        (EVENING, 'Evening'),
    ]

    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='availabilities')
    availability_day = models.CharField(max_length=20, choices=DAY_CHOICES, blank=True)
    availability_time = models.CharField(max_length=20, choices=TIME_CHOICES, blank=True)

    class Meta:
        verbose_name = 'Task Availability'
        verbose_name_plural = 'Task Availabilities'

    def __str__(self):
        return f'{self.task.title} Availability'


class Response(models.Model):
    PENDING = 'PENDING'
    ACCEPTED = 'ACCEPTED'
    DECLINED = 'DECLINED'
    COMPLETED = 'COMPLETED'
    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (ACCEPTED, 'Accepted'),
        (DECLINED, 'Declined'),
        (COMPLETED, 'Completed'),
    ]

    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    recipient = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='recipient')
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)
    created_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='created_by')
    created_on = models.DateTimeField(auto_now_add=True)
    resolved_on = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return 'Response to ' + self.task.title + ' by ' + self.created_by.username
