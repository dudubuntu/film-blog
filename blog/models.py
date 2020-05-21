from django.db import models
from django.shortcuts import reverse

from django.utils import timezone

from .fields import *


class Post(models.Model):
    title = models.CharField(max_length=250)
    description = models.CharField(max_length=500, blank=True)
    text = models.TextField(blank=True)
    poster = ThumbnailImageField(name="poster", upload_to='blog/images')
    add_date = models.DateTimeField(default=timezone.now)
    published = models.BooleanField(default=True)
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ['-add_date']
    
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={'slug': self.slug})


class Image(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='img')
    title = models.CharField(max_length=250)
    description = models.CharField(max_length=500, blank=True)
    img = ThumbnailImageField(name='image', upload_to='blog/images')

    def __str__(self):
        return self.title


class Tag(models.Model):
    post = models.ManyToManyField('Post', related_name='tag', blank=True)
    title = models.CharField(max_length=250)
    description = models.CharField(max_length=500, blank=True)
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ['title']
    
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:tag_detail', kwargs={'slug': self.slug})


class Discussion(models.Model):
    post = models.ManyToManyField('Post', related_name='discussion', blank=True)
    title = models.CharField(max_length=250)
    description = models.CharField(max_length=500, blank=True)
    add_date = models.DateTimeField(default=timezone.now)
    changed_date = models.DateTimeField(blank=True, null=True)
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ['-add_date']
    
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:discussion_detail', kwargs={'slug': self.slug})


class CommentPost(models.Model):
    post = models.ForeignKey('Post', related_name='comment_post', on_delete=models.CASCADE)
    user = models.ForeignKey('User', related_name='comment_post', on_delete=models.CASCADE)
    id = models.AutoField(primary_key=True)
    text = models.CharField(max_length=5000, blank=True)
    add_date = models.DateTimeField(default=timezone.now)
    changed_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ['-add_date']
    
    def __str__(self):
        return self.user.name

    def get_absolute_url(self):
        return reverse('blog:comment_post', kwargs={'id': self.id})


class CommentDiscussion(models.Model):
    discussion = models.ForeignKey('Discussion', related_name='comment_discussion', on_delete=models.CASCADE)
    user = models.ForeignKey('User', related_name='comment_discussion', on_delete=models.CASCADE)
    id = models.AutoField(primary_key=True)
    text = models.CharField(max_length=5000, blank=True)
    add_date = models.DateTimeField(default=timezone.now)
    changed_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ['-add_date']
    
    def __str__(self):
        return self.user.name

    def get_absolute_url(self):
        return reverse('blog:comment_discussion', kwargs={'id': self.id})


class User(models.Model):
    login = models.CharField(max_length=250, unique=True)
    name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250, blank=True)
    nickname = models.CharField(max_length=250, blank=True)
    age = models.PositiveIntegerField(blank=True)
    can_see_profile = models.BooleanField(default=True)
    permission = models.ForeignKey('Permission', related_name='user', to_field='id', on_delete=models.SET_DEFAULT, default=1)
    avatar = ThumbnailImageField(name='avatar', upload_to='blog/avatars')

    class Meta:
        ordering = ['login']

    def __str__(self):
        return self.nickname if self.nickname else ( f'{self.name}' + ' {0}'.format(self.last_name if self.last_name else '') )

    def get_absolute_url(self):
        return reverse('blog:profile_detail', kwargs={'slug': self.nickname if self.nickname else self.login})

class Permission(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.title

class UserHistory(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='history')
    date = models.DateTimeField()