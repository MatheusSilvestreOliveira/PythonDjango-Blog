from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView
from django.views import View
from .models import Post
from django.db.models import Q, Count, Case, When
from comments.forms import FormComment
from comments.models import Comments
from django.contrib import messages


class PostIndex(ListView):
    model = Post
    template_name = 'posts/index.html'
    context_object_name = 'posts'
    paginate_by = 3

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.select_related('post_category')
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
    template_name = 'posts/post_search.html'

    def get_queryset(self):
        qs = super().get_queryset()
        term = self.request.GET.get('term')
        if not term:
            return qs
        qs = qs.filter(
            Q(post_title__icontains=term) |
            Q(post_author__first_name__iexact=term) |
            Q(post_content__icontains=term) |
            Q(post_summary__icontains=term) |
            Q(post_category__cat_name__iexact=term)
        )
        return qs


class PostCategory(PostIndex):
    template_name = 'posts/post_category.html'

    def get_queryset(self):
        qs = super().get_queryset()
        category = self.kwargs.get('category', None)
        if not category:
            return qs
        qs = qs.filter(post_category__cat_name__iexact=category)
        return qs


class PostDetails(View):
    template_name = 'posts/post_details.html'

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        pk = self.kwargs.get('pk')
        post = get_object_or_404(Post, pk=pk, show_post=True)
        self.context = {
            'post': post,
            'comments': Comments.objects.order_by('-id').filter(comment_show=True, comment_post=post.id),
            'form': FormComment(request.POST or None),
        }

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        form = self.context['form']

        if not form.is_valid():
            return render(request, self.template_name, self.context)

        comment = form.save(commit=False)

        if request.user.is_authenticated:
            comment.comment_user = request.user

        comment.comment_post = self.context['post']
        comment.save()
        messages.success(self.request, 'Comment submitted successfully.')
        return redirect('post_details', pk=self.kwargs.get('pk'))


# class PostDetails(UpdateView):
#     template_name = 'posts/post_details.html'
#     model = Post
#     form_class = FormComment
#     context_object_name = 'post'
#
#     def form_valid(self, form):
#         post = self.get_object()
#         comment = Comments(**form.cleaned_data)
#         comment.comment_post = post
#
#         if self.request.user.is_authenticated:
#             comment.comment_user = self.request.user
#
#         comment.save()
#         messages.success(self.request, 'Comment submitted successfully.')
#
#         return redirect('post_details', pk=post.id)
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         post = self.get_object()
#         comments = Comments.objects.order_by('-id').filter(comment_show=True,
#                                            comment_post=post.id)
#         context['comments'] = comments
#         return context
