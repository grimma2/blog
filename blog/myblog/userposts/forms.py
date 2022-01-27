from django import forms
from django.core.exceptions import ValidationError

from .models import Post, Video, NewUser


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text')


class VideoForm(forms.ModelForm):

    class Meta:
        model = Video
        fields = ('title', 'description', 'video', 'import_video_url')

    def clean_import_video_url(self):
        data = self.cleaned_data
        if data['import_video_url'] and data['video']:
            raise ValidationError(
                'Заполненно должно быть только одно из полей - Файл видео или путь к видео'
            )
        return data['import_video_url']


class RegForm(forms.ModelForm):
    username = forms.CharField(label='Имя')
    password = forms.PasswordInput()

    class Meta:
        model = NewUser
        fields = ('username', 'password')
