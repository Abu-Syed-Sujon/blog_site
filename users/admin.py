from django.contrib import admin
from .models import Profile

# Register your models here.
@admin.register(Profile)
#admin.site.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    '''Admin view for user profile.'''
    list_display = ('user', 'bio', 'address', 'phone', 'profile_picture', 'birth_date')
    search_fields = ('user__username', 'bio', 'address', 'phone')
    list_filter = ('birth_date',)
    
