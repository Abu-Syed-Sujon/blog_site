from django.shortcuts import redirect, render
from django.contrib import messages
from .forms import UserRegisterForm
from django.contrib.auth.decorators import login_required

# Create your views here.

def registration_view(request):
    '''View for user registration.'''
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            form.save()
            messages.success(request, ' Your account has been created! You can now log in.')
            
            return redirect('login')  # Redirect to a success page or login page   
        #else:
          #  return render(request, 'users/registration.html', {'form': form})
    else:
        form = UserRegisterForm()
        
    return render(request, 'users/registration.html', {'form': form})

@login_required
def profile_view(request):
    '''View for user profile.'''
    return render(request, 'users/profile.html')
