from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.views import View
from django.views.generic import ListView, DetailView
from django.views.generic import FormView, CreateView, UpdateView, DeleteView
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.db import DatabaseError
from django.contrib import auth
from django.utils import timezone
from django.shortcuts import reverse
from django.shortcuts import redirect
from django.utils import timezone

from .models import *
from .forms import *


class Index(View):
    def get(self, request):
        return render(request, 'blog/index.html')


class Login(View):
    def get(self, request):
        print(dir(request.user))
        if request.user.is_authenticated:
            return redirect(reverse('blog:index'))
        else:
            return render(request, 'blog/login.html')
    
    def post(self, request):
        login = request.POST['login']
        user = auth.authenticate(request, username=login, password=request.POST['password'])
        if user is None:
            return render(request, 'blog/login.html', {'error': True})
        auth.login(request, user)
        UserHistory.objects.create(date=timezone.now(), user=User.objects.get(login=login))
        return redirect(reverse('blog:index'))


class Logout(View):
    def get(self, request):
        return render(request, 'blog/logout.html')

    def post(self, request):
        auth.logout(request)
        return redirect(reverse('blog:login'))


class PostList(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'post_list'

    def get_context_data(self, *args, object_list=None, **kwargs):
        context = super().get_context_data(*args, object_list=object_list, **kwargs)
        context['image_list'] = Image.objects.all()     # TODO разобраться, как выводить кадры
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        self.post = get_object_or_404(Post, slug=self.kwargs['slug'])
        context = super().get_context_data(**kwargs)
        context['tag_list'] = Tag.objects.filter(post=self.post)
        context['image_list'] = Image.objects.filter(post=self.post)
        context['comment_list'] = CommentPost.objects.filter(post=self.post)
        return context


class PostCreate(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_create.html'


class TagList(ListView):
    model = Tag
    template_name = 'blog/tag_list.html'
    context_object_name = 'tag_list'


class TagDetail(DetailView):
    model = Tag
    template_name = 'blog/tag_detail.html'
    context_object_name = 'tag'

    def get_context_data(self, **kwargs):
        self.tag = Tag.objects.get(slug=self.kwargs['slug'])
        context = super().get_context_data(**kwargs)
        context['post_list'] = Post.objects.filter(tag=self.tag)
        return context


class TagCreate(CreateView):
    model = Tag
    template_name = 'blog/tag_create.html'
    form_class = TagForm


class DiscussionList(ListView):
    model = Discussion
    template_name = 'blog/discussion_list.html'
    context_object_name = 'discussion_list'

    def get_context_data(self, *args, object_list=None, **kwargs):
        context = super().get_context_data(*args, object_list=object_list, **kwargs)
        context['post'] = Post.objects.all()
        context['comment_list'] = CommentDiscussion.objects.all()
        return context


class DiscussionDetail(DetailView):
    model = Discussion
    template_name = 'blog/discussion_detail.html'
    context_object_name = 'discussion'

    def get_context_data(self, **kwargs):
        self.dicussion = Discussion.objects.get(slug=self.kwargs['slug'])
        context = super().get_context_data(**kwargs)
        context['post_list'] = Post.objects.filter(discussion=self.dicussion)
        context['comment_list'] = CommentDiscussion.objects.filter(discussion=self.dicussion)
        context['comment_form'] = CommentDiscussionForm
        return context


class DiscussionCommentDetail(View):
    def post(self, request, slug):
        bound_form = CommentDiscussionForm(request.POST)

        if bound_form.is_valid():
            bound_form.add_date = timezone.now()
            bound_form.user = self.request.user
            bound_form.discussion = Discussion.objects.get(slug=slug)
            bound_form.save()

        return render(request, 'blog/discussion_detail.html')

    # model = CommentDiscussion
    # form_class = CommentDiscussionForm

    # def get_success_url(self):
    #     return reverse('blog.discussion_detail', kwargs={'slug': self.kwargs['slug']})

    # # def form_valid(self, form):
    # #     form.cleaned_data['add_date'] = timezone.now()
    # #     form.cleaned_data['user'] = self.request.user
    # #     form.cleaned_data['discussion'] = Discussion.objects.get(slug=self.kwargs['slug'])
    # #     return super().form_valid(form)

    # def post(self, request, *args, **kwargs):
    #     bound_form = CommentDiscussionForm(request.POST)

    #     if bound_form.is_valid():
    #         bound_form.save(commit=False)
    #         print()
    #         print()
    #         print(dir(bound_form))
    #         print(bound_form.fields)
    #         print()
    #         print()
    #         print()

    #         bound_form.fields['add_date'] = timezone.now()
    #         bound_form.fields['user'] = self.request.user
    #         bound_form.fields['discussion'] = Discussion.objects.get(slug=self.kwargs['slug'])
    #         bound_form.save()
    #         return redirect(self.success_url)
    #     return render(request, 'blog/discussion_detail.html')


class DiscussionCreate(CreateView):
    model = Discussion
    template_name = 'blog/discussion_create.html'
    form_class = DiscussionForm


class ProfileDetail(DetailView):
    model = User
    template_name = 'blog/profile_detail.html'
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        self.user = User.objects.get(login=self.kwargs['login'])
        context = super().get_context_data(**kwargs)
        context['discussion_list'] = Discussion.objects.filter(comment_discussion__user=self.user)
        context['post_list'] = Post.objects.filter(comment_post__user=self.user)
        return context