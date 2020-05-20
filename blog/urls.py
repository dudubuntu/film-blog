from django.urls import path

from .views import *


app_name = 'blog'
urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),

    path('posts/', PostList.as_view(), name='post_list'),
    path('post/<slug:slug>/', PostDetail.as_view(), name='post_detail'),

    path('post/#comment<int:id>/', PostList.as_view(), name='comment_post'),

    path('tags/', TagList.as_view(), name='tag_list'),
    path('tag/<slug:slug>/', TagDetail.as_view(), name='tag_detail'),

    path('discussions/', DiscussionList.as_view(), name='discussion_list'),
    path('discussion/<slug:slug>/', DiscussionDetail.as_view(), name='discussion_detail'),

    path('discussions/#comment<int:id>/', DiscussionList.as_view(), name='comment_discussion'),

    path('profile/<slug:slug>/', ProfileDetail.as_view(), name='profile_detail')
]