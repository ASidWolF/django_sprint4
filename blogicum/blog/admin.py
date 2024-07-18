from django.contrib import admin

from .models import Post, Category, Location, Comment


class PostAdmin(admin.ModelAdmin):
    list_display = (
        'is_published',
        'title',
        'text',
        'author',
        'location',
        'category',
        'pub_date',
    )
    list_editable = (
        'author',
        'pub_date',
    )
    search_fields = ('title',)
    list_filter = ('category', 'is_published',)
    list_display_links = ('title',)
    empty_value_diplay = 'Не задано'


class PostInline(admin.TabularInline):
    model = Post
    extra = 0


class CategoryAdmin(admin.ModelAdmin):
    inlines = (
        PostInline,
    )
    list_display = (
        'title',
    )


admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Location)
admin.site.register(Comment)
