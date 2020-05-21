from django import forms
from django.core.exceptions import FieldError, ValidationError

from .models import *
from .mixins import FormMixin

class PostForm(FormMixin):
    class Meta:
        model = Post
        fields = ('title', 'description', 'text', 'poster', 'slug')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'text': forms.Textarea(attrs={'class': 'form-control'}),
            'poster': forms.FileInput(attrs={'class': 'form-control-file'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
        }


class TagForm(FormMixin):
    class Meta:
        model = Tag
        fields = ('title', 'description', 'slug')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'})
        }


class DiscussionForm(FormMixin):
    class Meta:
        model = Discussion
        fields = ('title', 'description', 'post', 'slug')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'post': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'})
        }


class CommentDiscussionForm(forms.ModelForm):
    class Meta:
        model = CommentDiscussion
        fields = ('text',)
        widgets = {
            'text': forms.Textarea(attrs= {'class': 'form-control', 'height': '100'})
        }

    # def save(self, *args, **kwargs):
    #     form = super().save(commit=False)
    #     form.add_date = timezone.now()
    #     form.user = self.request.user
    #     form.discussion = Discussion.objects.get(slug=self.kwargs['slug'])
    #     form.save()