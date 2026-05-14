from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile

class UserRegisterForm(UserCreationForm):
    '''Form for user registration, extending Django's built-in UserCreationForm.'''
    
    email = forms.EmailField()

    class Meta:
        """Meta class for UserRegisterForm."""
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserUpdateForm(forms.ModelForm):
    '''Form for updating user information.'''
    
    email = forms.EmailField()

    class Meta:
        """Meta class for UserUpdateForm."""
        model = User
        fields = ['username', 'email']                      

class ProfileUpdateForm(forms.ModelForm):
    '''Form for updating user profile information.'''
    
    class Meta:
        """Meta class for ProfileUpdateForm."""
        model = Profile
        fields = ['bio', 'address', 'phone', 'profile_picture', 'birth_date']
        