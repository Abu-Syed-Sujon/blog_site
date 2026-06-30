'''views for the blog app. '''

from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (ListView, DetailView, CreateView, UpdateView, DeleteView)
from .models import Post



# Create your views here.


class PostListView(ListView):
    """View for listing blog posts on the home page."""
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-posted_at']

class PostDetailView(DetailView):
    """Detail view for a single blog post."""
    model = Post
    # template_name = 'blog/post_detail.html'

class PostCreateView(LoginRequiredMixin, CreateView):  # pylint: disable=too-many-ancestors
    """View for creating a new blog post."""
    model = Post
    template_name = 'blog/post_form.html'
    fields = ['title', 'content']
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):  # pylint: disable=too-many-ancestors
    """View for updating an existing blog post."""
    model = Post
    template_name = 'blog/post_form.html'
    fields = ['title', 'content']
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        post: Post = self.get_object()
        return self.request.user == post.author

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):  # pylint: disable=R0901
    """View for deleting a blog post (only the author may delete)."""
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = '/'

    def test_func(self):
        post: Post = self.get_object()
        return self.request.user == post.author

def about(request):
    '''View function for the about page.'''

    return render(request, 'blog/about.html', {'title': 'About'})

 
