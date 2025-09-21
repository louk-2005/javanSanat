# django files
from django.contrib import admin
from django.utils.html import format_html

# your files
from .models import Category, Article


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created_at')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    list_per_page = 20

    fieldsets = (
        (None, {
            'fields': ('name', 'slug')
        }),
        ('توضیحات', {
            'fields': ('description',),
            'classes': ('collapse',)
        }),
    )


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_thumbnail', 'author', 'category', 'created_at', 'is_updated')
    search_fields = ('title', 'excerpt', 'content')
    list_filter = ('category', 'author', 'created_at')
    prepopulated_fields = {'slug': ('title',)}
    list_per_page = 15
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at', 'updated_at', 'get_full_image')

    fieldsets = (
        (None, {
            'fields': ('title', 'slug')
        }),
        ('محتوا', {
            'fields': ('excerpt', 'content')
        }),
        ('تصویر', {
            'fields': ('featured_image', 'get_full_image'),
            'classes': ('collapse',)
        }),
        ('اطلاعات', {
            'fields': ('author', 'category', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def get_thumbnail(self, obj):
        if obj.featured_image:
            return format_html(
                '<img src="{}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 5px;" />',
                obj.featured_image.url
            )
        return "بدون تصویر"

    get_thumbnail.short_description = 'تصویر'

    def get_full_image(self, obj):
        if obj.featured_image:
            return format_html(
                '<img src="{}" style="max-width: 100%; height: auto; max-height: 300px;" />',
                obj.featured_image.url
            )
        return "بدون تصویر"

    get_full_image.short_description = 'پیش‌نمایش تصویر'

    def is_updated(self, obj):
        return obj.created_at != obj.updated_at

    is_updated.boolean = True
    is_updated.short_description = 'به‌روزرسانی شده؟'

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('author', 'category')