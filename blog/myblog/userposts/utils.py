from django.db.models import F
from django.http import HttpResponseRedirect
from django.views.generic.edit import ModelFormMixin
from django.contrib.contenttypes.models import ContentType

from .models import UserAction


class UserContentMixin(ModelFormMixin):

    def form_valid(self, form):
        data = form.cleaned_data
        model = self.form_class.Meta.model
        new_object = model.objects.create(
            **data | {'user': self.request.user, 'slug': data['title'].replace(' ', '-')}
        )

        return HttpResponseRedirect(new_object.get_absolute_url())


class CommentDataMixin:

    def comment_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        actions = self.object.actions.filter(user=self.request.user)
        if actions.exists():
            for act in actions:
                context[act.action] = True
        context['comments'] = self.object.comments.all()
        return context


class UserViewMixin:

    def view(self) -> None:
        self.model.objects.filter(slug=self.object.slug).update(views=F('views')+1)


class LikeDislikeActions:

    @staticmethod
    def add_model(user, act, obj):
        UserAction.objects.create(content_object=obj, action=act, user=user)

    @staticmethod
    def del_model(user, act, obj):
        obj.actions.get(action=act, user=user).delete()


class UserLikeDislike:

    def like(self, obj_slug, model, do) -> None:
        model = ContentType.objects.get(model=model.lower())
        for_update = model.model_class().objects.filter(slug=obj_slug)
        for_action = model.get_object_for_this_type(slug=obj_slug)
        if do == 'reduce':
            LikeDislikeActions.del_model(self.request.user, 'like', for_action)
            for_update.update(likes=F('likes')-1)
        elif do == 'add':
            LikeDislikeActions.add_model(self.request.user, 'like', for_action)
            for_update.update(likes=F('likes')+1)

    def dislike(self, obj_slug, model, do) -> None:
        model = ContentType.objects.get(model=model.lower())
        for_update = model.model_class().objects.filter(slug=obj_slug)
        for_action = model.get_object_for_this_type(slug=obj_slug)
        if do == 'reduce':
            LikeDislikeActions.del_model(self.request.user, 'dislike', for_action)
            for_update.update(dislikes=F('dislikes')-1)
        elif do == 'add':
            LikeDislikeActions.add_model(self.request.user, 'dislike', for_action)
            for_update.update(dislikes=F('dislikes')+1)
