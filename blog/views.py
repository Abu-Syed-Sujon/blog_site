'''views for the blog app. '''

from django.shortcuts import render
from .models import Post



# Create your views here.


def home(request):
    '''View function for the home page.'''
    context={
        'posts': Post.objects.all()  # pylint: disable=no-member
    }
    
    return render(request, 'blog/home.html', context)

def about(request):
    '''View function for the about page.'''

    return render(request, 'blog/about.html', {'title': 'About'})
