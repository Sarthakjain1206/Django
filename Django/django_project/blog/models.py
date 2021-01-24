from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

from django.urls import reverse

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now())

    # This line tells django that, if user gets deleted then delete all posts by that user and vice versa is not true.
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})