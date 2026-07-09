from django.shortcuts import redirect, render
from django.contrib import messages
from .forms import ProfileUpdateForm, UserRegisterForm, UserUpdateForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage
from .models import Profile
from .tokens import account_activation_token

# Create your views here.

def registration_view(request):
    '''View for user registration.'''
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            current_site = get_current_site(request)
            mail_subject = 'Activate your Django Blog account'
            message = render_to_string('users/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
                'protocol': 'https' if request.is_secure() else 'http',
            })
            from django.conf import settings

            email = EmailMessage(
                mail_subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
            )
            try:
                 email.send()
            except Exception as e:
                print("EMAIL ERROR:", repr(e))
                raise
            return redirect('account_activation_sent')
        
    else:
        form = UserRegisterForm()
        
    return render(request, 'users/registration.html', {'form': form})


def account_activation_sent_view(request):
    '''Show instructions after a registration activation email is sent.'''
    return render(request, 'users/account_activation_sent.html')


def activate_account_view(request, uidb64, token):
    '''Activate a user account from an email verification link.'''
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Your email has been verified. You can now log in.')
        return redirect('login')

    return render(request, 'users/account_activation_invalid.html')

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
