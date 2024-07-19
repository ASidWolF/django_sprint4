from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

from core.models import PublishedModel, CreatedAtModel


User = get_user_model()


class PostQuerySet(models.QuerySet):

    def with_related_data(self):
        return self.select_related('category', 'author')

    def default_filters(self):
        return self.filter(
            is_published=True,
            category__is_published=True,
            pub_date__lt=timezone.now(),
        )


class DefaultPostManager(models.Manager):

    def get_queryset(self):
        return (
            PostQuerySet(self.model).with_related_data().default_filters()
        )


class Category(PublishedModel, CreatedAtModel):
    title = models.CharField(max_length=256, verbose_name='Заголовок')
    description = models.TextField(verbose_name='Описание')
    slug = models.SlugField(
        verbose_name='Идентификатор',
        help_text=(
            'Идентификатор страницы для URL; разрешены символы'
            ' латиницы, цифры, дефис и подчёркивание.'
        ),
        unique=True,
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title


class Location(PublishedModel, CreatedAtModel):
    name = models.CharField(max_length=256, verbose_name='Название места')

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self):
        return self.name


class Post(PublishedModel, CreatedAtModel):
    title = models.CharField(max_length=256, verbose_name='Название')
    text = models.TextField(verbose_name='Текст')
    pub_date = models.DateTimeField(
        verbose_name='Дата и время публикации',
        help_text=(
            'Если установить дату и время в будущем'
            ' — можно делать отложенные публикации.'
        ),
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор публикации',
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Местоположение',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Категория',
    )
    image = models.ImageField(
        upload_to='posts_images',
        blank=True,
        verbose_name='Изображение',
    )

    objects = PostQuerySet.as_manager()
    default_filters = DefaultPostManager()

    @property
    def comment_count(self):
        return self.comment.count()

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        related_name='comment',
        on_delete=models.CASCADE,
        verbose_name='Публикация',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор публикации',
    )
    text = models.TextField(
        verbose_name='Текст',
        help_text='Ваш комментарий можете написать здесь!'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата и время комментария',
    )

    class Meta:
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('created_at',)

    def __str__(self):
        return f'Комментарий пользователя {self.author}'
