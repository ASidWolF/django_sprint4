from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse

from .models import Post, Comment


class GetSuccessUrlPostDetailMixin:

    def get_success_url(self):
        return reverse(
            'blog:post_detail', kwargs={'post_id': self.kwargs['post_id']}
        )


class CommentMixin(LoginRequiredMixin, GetSuccessUrlPostDetailMixin):
    model = Comment
    template_name = 'blog/comment.html'
    pk_url_kwarg = 'comment_id'

    def dispatch(self, request, *args, **kwargs):
        comment = get_object_or_404(Comment, pk=self.kwargs['comment_id'])
        if comment.author != request.user:
            return redirect(
                'blog:post_detail', post_id=self.kwargs['post_id']
            )
        return super().dispatch(request, *args, **kwargs)


class PostMixin(LoginRequiredMixin):
    model = Post
    template_name = 'blog/create.html'
    pk_url_kwarg = 'post_id'

    def dispatch(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        if post.author != request.user:
            return redirect(
                'blog:post_detail', post_id=self.kwargs['post_id']
            )
        return super().dispatch(request, *args, **kwargs)


class PaginationMixin:

    def paginate_queryset(self, queryset, page_size=settings.POSTS_PER_PAGE):
        paginator = Paginator(queryset, page_size)
        page = self.request.GET.get('page')
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)
        return posts
