from django.urls import path

from .views import *


app_name = 'blog'
urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),

    path('posts/', PostList.as_view(), name='post_list'),
    path('post/create/', PostCreate.as_view(), name='post_create'),
    path('post/<slug:slug>/', PostDetail.as_view(), name='post_detail'),

    path('post/#comment<int:id>/', PostList.as_view(), name='comment_post'),    #TODO добавить возможность переходить к комментарию

    path('tags/', TagList.as_view(), name='tag_list'),
    path('tag/create/', TagCreate.as_view(), name='tag_create'),
    path('tag/<slug:slug>/', TagDetail.as_view(), name='tag_detail'),

    path('discussions/', DiscussionList.as_view(), name='discussion_list'),
    path('discussion/create/', DiscussionCreate.as_view(), name='discussion_create'),
    path('discussion/<slug:slug>/', DiscussionDetail.as_view(), name='discussion_detail'),  
    path('discussion/<slug:slug>/comment', DiscussionCommentDetail.as_view(), name='discussion_comment_detail'),    

    path('discussions/#comment<int:id>/', DiscussionList.as_view(), name='comment_discussion'),     #TODO добавить возможность переходить к комментарию

    path('profile/<slug:login>/', ProfileDetail.as_view(), name='profile_detail')
]