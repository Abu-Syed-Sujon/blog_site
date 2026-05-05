from django.shortcuts import redirect, render
from django.contrib import messages
from .forms import UserRegisterForm

# Create your views here.

def registration_view(request):
    '''View for user registration.'''
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            form.save()
            messages.success(request, f'Account created for {username} successfully!')
            
            return redirect('blog-home')  # Redirect to a success page or login page   
        #else:
          #  return render(request, 'users/registration.html', {'form': form})
    else:
        form = UserRegisterForm()
        
    return render(request, 'users/registration.html', {'form': form})
