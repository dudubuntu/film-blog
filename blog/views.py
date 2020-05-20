from django.shortcuts import render
from django.views import View
from django.views.generic import ListView, DetailView, FormView

from .models import *


class Index(View):
    def get(self, request):
        return render(request, 'blog/index.html')


class Login(FormView):
    pass


class Logout(View):
    pass


class PostList(ListView):
    model = Post


class PostDetail(DetailView):
    pass


class TagList(ListView):
    pass


class TagDetail(ListView):
    pass


class DiscussionList(ListView):
    model = Discussion


class DiscussionDetail(DetailView):
    pass


class ProfileDetail(DetailView):
    pass