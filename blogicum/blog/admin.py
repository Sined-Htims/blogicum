from django.contrib import admin

from .models import Category, Comments, Location, Post

admin.site.register(Location)


class PostInline(admin.StackedInline):
    model = Post
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    inlines = (
        PostInline,
    )
    list_display = (
        'title',
        'is_published',
        'slug',
        'created_at',
    )
    list_editable = ('is_published',)
    search_fields = ('title',)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'is_published',
        'category',
        'author',
        'location',
        'created_at',
        'pub_date',
    )
    list_editable = (
        'is_published',
        'category',
    )
    list_filter = ('category',)
    search_fields = ('title',)


@admin.register(Comments)
class Comments(admin.ModelAdmin):
    list_display = (
        'text',
        'post',
        'created_at',
        'author',
    )
    list_filter = ('post',)
    search_fields = ('author',)
