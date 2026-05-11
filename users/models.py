from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    '''Model for user profile.'''
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    address = models.CharField(max_length=30, blank=True)
    phone = models.CharField(max_length=15, blank=True)
    profile_picture = models.ImageField(default='profile_pics/default.jpg', upload_to='profile_pics/', blank=True)
    birth_date = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return f'{self.user} Profile'
    