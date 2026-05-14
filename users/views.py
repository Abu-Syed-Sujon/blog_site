from django.shortcuts import redirect, render
from django.contrib import messages
from .forms import ProfileUpdateForm, UserRegisterForm, UserUpdateForm
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from .models import Profile

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

@login_required
def profile_update_view(request):
    '''View for updating user profile.'''
    # Safely get or create the profile for existing users
    
    user_profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, ' Your account has been updated!')
            return redirect('profile')  # Redirect to profile page after update
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    
    context = {
        'u_form': u_form,
        'p_form': p_form,
    }
    
    return render(request, 'users/profile_update.html', context)