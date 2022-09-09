from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView
from .models import Post
from django.db.models import Q, Count, Case, When


class PostIndex(ListView):
    model = Post
    template_name = 'posts/index.html'
    context_object_name = 'posts'
    paginate_by = 3

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.order_by('-id').filter(show_post=True)
        qs = qs.annotate(
            num_commentaries=Count(
                Case(
                    When(comments__comment_show=True, then=1)
                )
            )
        )
        return qs


class PostSearch(PostIndex):
    pass


class PostCategory(PostIndex):
    pass


class PostDetails(UpdateView):
    pass
