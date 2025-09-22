# django files
from django.contrib import admin
from django.utils.html import format_html,mark_safe

# your files
from .models import Category, Article,CourseInfo, CourseImage
from django.utils.translation import gettext_lazy as _


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




# Inline برای مدیریت تصاویر دوره
class CourseImageInline(admin.TabularInline):
    model = CourseImage
    extra = 1
    fields = ('caption', 'image', 'image_preview')
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="100" height="auto" />')
        return _("No Image")
    image_preview.short_description = 'Preview'

@admin.register(CourseInfo)
class CourseInfoAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'base_image_preview', 'teachers', 'start_date', 'end_date',
                   'duration', 'price_display', 'discount_display', 'final_price_display',
                   'is_published', 'created_at')
    list_filter = ('is_published', 'created_at', 'start_date', 'end_date')
    search_fields = ('title', 'slug', 'description', 'teachers')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('base_image_preview', 'final_price_display', 'created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'description', 'teachers')
        }),
        (_('Dates & Duration'), {
            'fields': ('start_date', 'end_date', 'duration'),
            'classes': ('collapse',)
        }),
        (_('Pricing'), {
            'fields': ('price', 'discount', 'final_price_display'),
            'description': _('Final price is calculated automatically')
        }),
        (_('Image'), {
            'fields': ('base_image', 'base_image_preview')
        }),
        (_('Publication'), {
            'fields': ('is_published',)
        }),
        (_('Timestamps'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    inlines = [CourseImageInline]

    def base_image_preview(self, obj):
        if obj.base_image:
            return mark_safe(f'<img src="{obj.base_image.url}" width="200" height="auto" />')
        return _("No Image")
    base_image_preview.short_description = 'Base Image Preview'

    def price_display(self, obj):
        return f"{obj.price:,.0f} تومان"
    price_display.short_description = 'Price'
    price_display.admin_order_field = 'price'

    def discount_display(self, obj):
        if obj.discount:
            return f"{obj.discount:,.0f} تومان"
        return "-"
    discount_display.short_description = 'Discount'
    discount_display.admin_order_field = 'discount'

    def final_price_display(self, obj):
        if obj.final_price is None:
            return "-"
        return f"{obj.final_price:,.0f} تومان"

    final_price_display.short_description = 'Final Price'
    final_price_display.admin_order_field = 'final_price'

@admin.register(CourseImage)
class CourseImageAdmin(admin.ModelAdmin):
    list_display = ('caption', 'image_preview', 'course_link', 'created_at')
    list_filter = ('course', 'created_at')
    search_fields = ('caption', 'course__title')
    readonly_fields = ('image_preview', 'created_at', 'updated_at')

    def image_preview(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="100" height="auto" />')
        return _("No Image")
    image_preview.short_description = 'Preview'

    def course_link(self, obj):
        url = f"/admin/course/courseinfo/{obj.course.id}/change/"
        return format_html('<a href="{}">{}</a>', url, obj.course.title)
    course_link.short_description = 'Course'
    course_link.admin_order_field = 'course__title'







