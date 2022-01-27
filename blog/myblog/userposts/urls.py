from django.urls import path
from .views import *


urlpatterns = [
    path('', base_view, name='base_page'),
    path('posts/<str:slug>/', PostDetail.as_view(), name='post_detail'),
    path('videos/<str:slug>/', VideoDetail.as_view(), name='video_detail'),
    path('createpost/', CreatePostView.as_view(), name='post_form'),
    path('createvideo/', CreateVideoView.as_view(), name='video_form'),
    path('createcomment/<str:obj_slug>/<str:model>/', create_comment, name='create_comment'),
    path('posts/', PostList.as_view(), name='posts'),
    path('videos/', VideoList.as_view(), name='videos'),
    path('useraction/<act>/<model>/<str:obj_slug>/<do>/',
         UserActionView.as_view(), name='user_action'),
    path('loadobjects/', dynamic_load, name='load_objects'),

    path('register/', RegisterView.as_view(), name='register'),
    path('login/', AuthView.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
]