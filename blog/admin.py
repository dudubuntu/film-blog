from django.contrib import admin

from .models import *


class CommentPostInLine(admin.StackedInline):
    model = CommentPost
    fields = ('post', 'user', 'text', ('id', 'add_date', 'changed_date'))
    extra = 1
    view_on_site = True ########################### TO DO проверить


class ImageInLine(admin.TabularInline):
    model = Image
    fields = ('post', 'title', 'description', 'img')
    extra = 1


class CommentDiscussionInLine(admin.StackedInline):
    model = CommentDiscussion
    fields = ('discussion', 'user', 'text', ('id', 'add_date', 'changed_date'))
    extra = 1
    view_on_site = True ########################### TO DO проверить


class UserInLine(admin.StackedInline):
    model = User
    fieldsets = (
        ('User', {
            'classes': ('collapse',),
            'fields': ('name', 'last_name', 'nickname'),
        }),
        ('Optional', {
            'classes': ('collapse',),
            'fields': ('age', 'can_see_profile', 'permission', 'avatar'),
        }),
        ('Login data', {
            'classes': ('collapse',),
            'fields': ('login', 'password'),
        })
    )
    extra = 1
    view_on_site = True ########################### TO DO проверить

class UserHistoryInLine(admin.TabularInline):
    model = UserHistory
    fields = ('date',)
    extra = 1


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    model = Post
    date_hierarchy = 'add_date'
    fields = ('title', 'description', 'text', 'poster', ('add_date', 'published', 'slug'))
    list_display = ('title', 'slug', 'published')
    list_editable = ('published',)
    search_list = ('title', 'slug', 'text')
    list_filter = ('add_date', 'published')
    inlines = (ImageInLine, CommentPostInLine)
    view_on_site = True


@admin.register(Discussion)
class DiscussionAdmin(admin.ModelAdmin):
    model = Discussion
    date_hierarchy = 'add_date'
    fields = ('post', 'title', 'description', ('add_date', 'changed_date', 'slug'))
    list_filter = ('post', 'add_date', 'changed_date')
    search_list = ('title', 'description', 'slug')
    view_on_site = True
    inlines = (CommentDiscussionInLine,)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    model = Tag
    view_on_site = True


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    model = User
    fieldsets = (
        (None, {
            'fields': ('name', 'last_name', 'nickname'),
        }),
        ('Optional', {
            'fields': ('age', 'can_see_profile', 'permission', 'avatar'),
        }),
        ('Login data', {
            'classes': ('collapse',),
            'fields': ('login', 'password'),
        })
    )
    display_list = ('name', 'last_name', 'nickname', 'login')
    search_list = ('name', 'last_name', 'nickname', 'login')
    list_filter = ('age', 'can_see_profile', 'permission')
    view_on_site = True
    inlines = (CommentPostInLine, CommentDiscussionInLine, UserHistoryInLine)


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    model = Permission
    inlines = [UserInLine]