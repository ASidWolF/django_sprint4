from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import (
    ListView, DetailView, UpdateView, DeleteView, CreateView,
)

from .forms import CommentForm, PostForm
from .models import Post, Category, Comment


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


class PostListView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'page_obj'
    queryset = Post.default_filters.order_by('-pub_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = Paginator(context['page_obj'], settings.POSTS_PER_PAGE)
        page = self.request.GET.get('page')

        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)

        context['page_obj'] = posts
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    pk_url_kwarg = 'post_id'

    def get_object(self, queryset=None):
        obj = get_object_or_404(
            self.model.objects,
            pk=self.kwargs['post_id']
        )
        author = obj.author
        if author != self.request.user:
            obj = get_object_or_404(
                Post.default_filters,
                pk=self.kwargs['post_id']
            )

        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        post = self.get_object()
        comments = Comment.objects.filter(post=post)
        context['comments'] = comments

        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:profile', args=[self.request.user])


class PostUpdateView(PostMixin, UpdateView):
    form_class = PostForm

    def get_success_url(self):
        return reverse(
            'blog:post_detail', kwargs={'post_id': self.kwargs['post_id']}
        )


class PostDeleteView(PostMixin, DeleteView):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = PostForm(instance=self.object)
        return context

    def get_success_url(self):
        return reverse("blog:profile", kwargs={"username": self.request.user})


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    template_name = 'blog/comment.html'
    form_class = CommentForm

    def get_context_data(self, **kwargs):
        return dict(**super().get_context_data(**kwargs), form=CommentForm())

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            'blog:post_detail', kwargs={'post_id': self.kwargs['post_id']}
        )


class CommentMixin(LoginRequiredMixin):
    model = Comment
    template_name = 'blog/comment.html'
    pk_url_kwarg = 'comment_id'

    def get_success_url(self):
        return reverse(
            'blog:post_detail', kwargs={'post_id': self.kwargs['post_id']}
        )

    def dispatch(self, request, *args, **kwargs):
        comment = get_object_or_404(Comment, pk=self.kwargs['comment_id'])
        if comment.author != request.user:
            return redirect(
                'blog:post_detail', post_id=self.kwargs['post_id']
            )
        return super().dispatch(request, *args, **kwargs)


class CommentUpdateView(CommentMixin, UpdateView):
    form_class = CommentForm


class CommentDeleteView(CommentMixin, DeleteView):
    pass

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     del context['form']
    #     return context


class UserDetailView(DetailView):
    model = User
    template_name = 'blog/profile.html'
    context_object_name = 'profile'
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile_posts = Post.objects.filter(
            author=self.get_object()
        ).order_by('-pub_date')
        author = self.kwargs['username']
        if author != self.request.user.username:
            profile_posts = Post.default_filters.filter(
                author=self.get_object()
            ).order_by('-pub_date')
        paginator = Paginator(profile_posts, settings.POSTS_PER_PAGE)
        page = self.request.GET.get('page')
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)

        context['page_obj'] = posts
        return context

    def get_object(self, queryset=None):
        return get_object_or_404(User, username=self.kwargs['username'])


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    slug_field = 'username'
    slug_url_kwarg = 'username'
    template_name = 'blog/user.html'
    fields = ['first_name', 'last_name', 'email']

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy(
            'blog:profile', kwargs={'username': self.request.user.username}
        )


class CategoryPostsListView(ListView):
    model = Post
    template_name = 'blog/category.html'
    context_object_name = 'page_obj'

    def get_queryset(self):
        return Post.default_filters.filter(
            category__slug=self.kwargs['category_slug']
        ).order_by('-pub_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = Paginator(self.object_list, settings.POSTS_PER_PAGE)
        page = self.request.GET.get('page')

        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)

        category = get_object_or_404(
            Category, slug=self.kwargs['category_slug'], is_published=True
        )

        context['category'] = category
        context['page_obj'] = posts
        return context
