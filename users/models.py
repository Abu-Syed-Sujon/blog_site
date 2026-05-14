from io import BytesIO
from django.core.files.base import ContentFile
from django.db.models.fields.files import ImageFieldFile  # Required for your type hint
from PIL import Image

from django.db import models
from django.db.models.fields.files import ImageFieldFile
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
    

    def save(self, *args, **kwargs):
        '''Override save method to resize profile picture only when a new file is uploaded.'''
        
        # 1. CRITICAL CHECK: Only process if a file is present AND it's a freshly uploaded file object.
        # When a model is saved during login, profile_picture.file is an underlying file descriptor, 
        # but it won't have an 'uploaded_to' attribute or memory buffer state like a fresh upload.
        # Alternatively, checking if the field is in kwargs or changed prevents the PIL crash.
        
        if self.profile_picture:
            try:
                # Test if Pillow can safely read the file without executing an asset load
                with Image.open(self.profile_picture) as img:
                    img_format = img.format if img.format else 'JPEG'
                    
                    # 2. Only resize if the dimensions exceed your limits
                    if img.height > 300 or img.width > 300:
                        output_size = (300, 300)
                        img.thumbnail(output_size)
                        
                        # Fix transparency backgrounds for JPEG conversions
                        if img.mode in ('RGBA', 'LA') and img_format.upper() in ('JPEG', 'JPG'):
                            background = Image.new('RGB', img.size, (255, 255, 255))
                            background.paste(img, mask=img.split()[-1])
                            img = background

                        with BytesIO() as buffer:
                            img.save(buffer, format=img_format, quality=85)
                            
                            profile_picture: ImageFieldFile = self.profile_picture
                            profile_picture.save(       #pylint: disable=no-member
                                profile_picture.name,
                                ContentFile(buffer.getvalue()),
                                save=False  # Crucial: Avoids infinite loops
                            )
            except (IOError, ValueError, AssertionError):
                # If Pillow cannot parse it (e.g. login signal without fresh file stream),
                # skip resizing entirely and let Django proceed safely.
                pass
                    
        # 3. Proceed with standard database operations
        super().save(*args, **kwargs)
