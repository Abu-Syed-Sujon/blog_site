'''views for the blog app. '''

from django.shortcuts import render



# Create your views here.
posts= [
    {
        'author': 'John Doe',
        'title': 'First Post',
        'content': 'This is the content of the first post.',
        'date_posted': 'June 1, 2024'
    },
    {
        'author': 'Jane Smith',
        'title': 'Second Post',
        'content': 'This is the content of the second post.',
        'date_posted': 'June 2, 2024'
    }
]

def home(request):
    '''View function for the home page.'''
    context={
        'posts': posts
    }
    
    return render(request, 'blog/home.html', context)

def about(request):
    '''View function for the about page.'''

    return render(request, 'blog/about.html', {'title': 'About'})
