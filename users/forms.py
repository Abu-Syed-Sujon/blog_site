from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserRegisterForm(UserCreationForm):
    '''Form for user registration, extending Django's built-in UserCreationForm.'''
    
    email = forms.EmailField()

    class Meta:
        """Meta class for UserRegisterForm."""
        model = User
        fields = ['username', 'email', 'password1', 'password2']
