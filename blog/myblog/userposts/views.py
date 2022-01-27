from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, DetailView, ListView, View
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.contenttypes.models import ContentType

from .models import Post, Video, Comment, UserAction
from .forms import PostForm, VideoForm, RegForm
from .utils import (
    UserContentMixin, CommentDataMixin, UserLikeDislike, UserViewMixin
)


class RegisterView(CreateView):
    form_class = RegForm
    template_name = 'userposts/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        login(self.request, form.save())
        return redirect('base_page')


class AuthView(LoginView):
    form_class = AuthenticationForm
    template_name = 'userposts/login.html'
    success_url = reverse_lazy('base_page')


def logout_user(request):
    logout(request)
    return redirect('base_page')


def base_view(request):
    posts = Post.objects.get_most_views()
    videos = Video.objects.get_most_views()
    return render(request, 'userposts/index.html', {'videos': videos, 'posts': posts})


class PostDetail(UserViewMixin, CommentDataMixin, DetailView):
    model = Post
    template_name = 'userposts/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        self.view()
        return self.comment_context_data(**kwargs)


class VideoDetail(UserViewMixin, CommentDataMixin, DetailView):
    model = Video
    template_name = 'userposts/video_detail.html'
    context_object_name = 'video'

    def get_context_data(self, **kwargs):
        self.view()
        return self.comment_context_data(**kwargs)


def create_comment(request, obj_slug, model):
    obj = ContentType.objects.get(model=model.lower()).get_object_for_this_type(slug=obj_slug)
    Comment.objects.create(
        content_object=obj,
        user=request.user,
        text=request.POST['text']
    )

    return HttpResponseRedirect(obj.get_absolute_url())


class CreatePostView(UserContentMixin, CreateView):
    form_class = PostForm
    template_name = 'userposts/post_form.html'


class CreateVideoView(UserContentMixin, CreateView):
    form_class = VideoForm
    template_name = 'userposts/video_form.html'


class PostList(ListView):
    template_name = 'userposts/post_list.html'
    context_object_name = 'posts'
    queryset = Post.objects.get_most_views()


class VideoList(ListView):
    template_name = 'userposts/video_list.html'
    context_object_name = 'videos'
    queryset = Video.objects.get_most_views()


class UserActionView(UserLikeDislike, View):

    def get(self, request, act, obj_slug, model, do):
        if act == 'like':
            self.like(obj_slug, model, do)
        elif act == 'dislike':
            self.dislike(obj_slug, model, do)

        return JsonResponse({'data': False})


def dynamic_load(request):
    model = ContentType.objects.get(model=list(request.GET.keys())[1].lower()).model_class()
    objects = list(model.objects.filter(pk__gt=int(request.GET['last_id'][0])).values())[:2]
    if objects:
        for obj in objects:
            obj['url'] = reverse('post_detail', kwargs={'slug': obj['slug']})
            del obj['slug']

        objects[-1]['last-object'] = True
        return JsonResponse({'data': {'values': objects}})
    else:
        return JsonResponse({'data': False})
