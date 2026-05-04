from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Post(models.Model):
    '''Model representing a blog post.'''
    title = models.CharField(max_length=200)
    content = models.TextField()
    posted_at = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.title)
