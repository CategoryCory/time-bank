from django.db import models
from django.contrib.auth import get_user_model


class UserReview(models.Model):
    rating = models.FloatField(default=0.0)
    comments = models.CharField(max_length=200, blank=True)
    reviewee = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='reviewee')
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='author')
    created_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.author.username} -> {self.reviewee.username}'
