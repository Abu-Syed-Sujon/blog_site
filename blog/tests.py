from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Post


class PostListViewPaginationTests(TestCase):
    """Tests for pagination on the blog home feed."""

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='testuser', password='password')
        for index in range(7):
            Post.objects.create(
                title=f'Post {index}',
                content='Test content',
                author=cls.user,
                posted_at=timezone.now() - timezone.timedelta(days=index),
            )

    def test_home_page_shows_first_five_posts(self):
        response = self.client.get(reverse('blog-home'))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['is_paginated'])
        self.assertEqual(len(response.context['posts']), 5)
        self.assertContains(response, 'Next')

    def test_second_page_shows_remaining_posts(self):
        response = self.client.get(f"{reverse('blog-home')}?page=2")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['posts']), 2)
        self.assertContains(response, 'Previous')


class UserListViewTests(TestCase):
    """Tests for the specific-user blog post list."""

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create_user(username='author', password='password')
        cls.other_author = User.objects.create_user(username='other', password='password')
        for index in range(6):
            Post.objects.create(
                title=f'Author Post {index}',
                content='Author content',
                author=cls.author,
                posted_at=timezone.now() - timezone.timedelta(days=index),
            )
        Post.objects.create(
            title='Other Author Post',
            content='Other content',
            author=cls.other_author,
        )

    def test_user_posts_page_shows_only_selected_user_posts(self):
        response = self.client.get(reverse('user-posts', kwargs={'username': 'author'}))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['post_author'], self.author)
        self.assertEqual(len(response.context['posts']), 5)
        self.assertContains(response, 'Posts by author')
        self.assertContains(response, 'Author Post')
        self.assertNotContains(response, 'Other Author Post')

    def test_user_posts_page_returns_404_for_unknown_user(self):
        response = self.client.get(reverse('user-posts', kwargs={'username': 'missing'}))

        self.assertEqual(response.status_code, 404)
