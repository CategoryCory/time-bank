from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.urls import reverse


class CustomUser(AbstractUser):
    date_of_birth = models.DateField(default=timezone.now)
    is_approved = models.BooleanField(verbose_name='Approved',
                                      help_text='Designates whether this user has been approved to post on this site.',
                                      default=False)
    address_street = models.CharField(verbose_name='Street Address', max_length=200)
    address_city = models.CharField(verbose_name='City', max_length=75)
    address_state = models.CharField(verbose_name='State', max_length=50)
    address_zip = models.CharField(verbose_name='ZIP Code', max_length=50)
    biography = models.TextField()
    skills = models.TextField()
    social_facebook = models.URLField(verbose_name='Facebook', max_length=200, blank=True)
    social_twitter = models.URLField(verbose_name='Twitter', max_length=200, blank=True)
    social_instagram = models.URLField(verbose_name='Instagram', max_length=200, blank=True)
    social_linkedin = models.URLField(verbose_name='LinkedIn', max_length=200, blank=True)
    profile_pic = models.ImageField(upload_to='images/')
    sullivan_coins_balance = models.FloatField(default=5.0)

    def __str__(self):
        return self.email

    def get_absolute_url(self):
        return reverse('users:user_detail', args=[self.username])
