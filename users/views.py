from django.shortcuts import redirect, render
from django.contrib import messages
from .forms import UserRegisterForm
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.

def registration_view(request):
    '''View for user registration.'''
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, ' Your account has been created! You can now log in.')
            
            return redirect('login')  # Redirect to a success page or login page   
        
    else:
        form = UserRegisterForm()
        
    return render(request, 'users/registration.html', {'form': form})

@login_required
def profile_view(request):
    '''View for user profile.'''
    try:
        user_profile = request.user.profile
    except ObjectDoesNotExist:
        user_profile = None  # Now the view won't crash!
    
    return render(request, 'users/profile.html', {'user_profile': user_profile})
