from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType

from myblog.settings import AUTH_USER_MODEL

from embed_video.fields import EmbedVideoField


class GetMostPopularManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset()

    def get_most_views(self):
        return self.get_queryset().order_by('-views')[:30]

    def get_most_likes(self):
        return self.get_queryset().order_by('-likes')[:30]


class SingleUserData(models.Model):
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)
    views = models.PositiveIntegerField(default=0)

    objects = GetMostPopularManager()

    def get_absolute_url(self):
        return reverse(
            f'{self.__class__.__name__.lower()}_detail', kwargs={'slug': self.slug}
        )

    class Meta:
        abstract = True


class Post(SingleUserData):
    title = models.CharField('Заголовок', max_length=299, unique=True)
    text = models.TextField('Текст')
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    slug = models.CharField('URL', max_length=499)
    comments = GenericRelation(
        'Comment', content_type_field='content_type', object_id_field='object_id'
    )
    actions = GenericRelation(
        'UserAction', content_type_field='content_type', object_id_field='object_id'
    )

    def __str__(self):
        return str(self.title)


class Video(SingleUserData):
    video = models.FileField('Видео', upload_to='videos/%Y/%m/%d', blank=True, null=True)
    import_video_url = EmbedVideoField(blank=True)
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField('Название видео', max_length=255, unique=True)
    description = models.TextField('Описание', blank=True, null=True)
    slug = models.CharField('URL', max_length=499)
    comments = GenericRelation(
        'Comment', content_type_field='content_type', object_id_field='object_id'
    )
    actions = GenericRelation(
        'UserAction', content_type_field='content_type', object_id_field='object_id'
    )

    def __str__(self):
        return str(self.title)


class Comment(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField('Текст коментария')

    def __str__(self):
        return str(self.text)


class UserAction(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    content_object = GenericForeignKey('content_type', 'object_id')
    action = models.CharField('Действие пользователя', max_length=10)


class NewUser(AbstractUser, SingleUserData):
    subscribers = models.ManyToManyField('self', symmetrical=False, blank=True)
