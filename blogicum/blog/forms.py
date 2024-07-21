from django.forms import ModelForm, DateTimeInput, Textarea

from .models import Comment, Post


class CommentForm(ModelForm):

    class Meta:
        model = Comment
        fields = ('text',)
        widgets = {
            'text': Textarea({'rows': '3'})
        }


class PostForm(ModelForm):

    class Meta:
        model = Post
        exclude = ('author', 'created_at',)
        widgets = {
            'pub_date': DateTimeInput(
                format='%Y-%m-%dT%H:%M', attrs={'type': 'datetime-local'}
            ),
            'text': Textarea({'rows': '5'}),
        }
