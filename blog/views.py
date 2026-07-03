"""Views for the blog app."""

from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, render
from django.views.generic import (ListView, DetailView, CreateView, UpdateView, DeleteView)

from .models import Post


class PostListView(ListView):
    """View for listing blog posts on the home page."""
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-posted_at']
    # Show five posts per page on the blog home feed.
    paginate_by = 5


class UserListView(ListView):
    """View for listing blog posts by a specific user."""
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    ordering = ['-posted_at']
    # Show five posts per page on the specific-user feed.
    paginate_by = 5

    def get_queryset(self):
        """Return posts written by the selected user."""
        # Specific-user list: fetch the user first so unknown usernames return 404.
        self.post_author = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=self.post_author).order_by('-posted_at')  # type: ignore[attr-defined]

    def get_context_data(self, **kwargs):
        """Add the selected post author to the template context."""
        context = super().get_context_data(**kwargs)
        context['post_author'] = self.post_author
        return context


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
    """View function for the about page."""

    return render(request, 'blog/about.html', {'title': 'About'})
