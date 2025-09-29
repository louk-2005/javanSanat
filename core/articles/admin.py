# django files
from django.contrib import admin
from django.utils.html import format_html,mark_safe
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.db.models import Count

# your files
from .models import Category, Article,CourseInfo, CourseImage, VideoCast, IndustrialTourism, IndustrialTourismImages


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





@admin.register(VideoCast)
class VideoCastAdmin(admin.ModelAdmin):
    # لیست در صفحه اصلی
    list_display = (
        'title',
        'order',
        'created_at',
        'updated_at',
        'video_link',
        'video_preview',
    )
    list_display_links = ('title',)
    list_filter = ('created_at', 'updated_at')
    search_fields = ('title', 'aparat_url')
    ordering = ('order', 'created_at')

    # تنظیمات فرم
    fieldsets = (
        (None, {
            'fields': ('title', 'aparat_url', 'order'),
            'description': 'جزئیات ویدیو و لینک آپارات را وارد کنید'
        }),
        ('اطلاعات سیستمی', {
            'fields': ('aparat_id', 'created_at', 'updated_at'),
            'classes': ('collapse',),
            'description': 'به‌صورت خودکار تولید می‌شود'
        }),
        ('پیش‌نمایش', {
            'fields': ('embed_preview', 'thumbnail_preview'),
            'classes': ('collapse',),
            'description': 'پیش‌نمایش ویدیو (خودکار)'
        }),
    )
    readonly_fields = (
        'aparat_id',
        'created_at',
        'updated_at',
        'embed_preview',
        'thumbnail_preview',
    )

    # متدهای نمایش
    @admin.display(description='لینک ویدیو')
    def video_link(self, obj):
        if obj.aparat_id:
            return format_html(
                '<a href="{}" target="_blank" rel="noopener noreferrer">'
                '<i class="fas fa-external-link-alt"></i> مشاهده در آپارات</a>',
                obj.aparat_url
            )
        return "ندارد"

    @admin.display(description='پیش‌نمایش ویدیو')
    def video_preview(self, obj):
        if obj.aparat_id:
            return mark_safe(
                f'<iframe src="{obj.embed_url}" width="300" height="200" frameborder="0" allowfullscreen></iframe>'
            )
        return "ذخیره کنید تا نمایش داده شود"

    @admin.display(description='Embed Preview')
    def embed_preview(self, obj):
        if obj.aparat_id:
            return mark_safe(
                f'<iframe width="560" height="315" src="{obj.embed_url}" '
                'frameborder="0" allowfullscreen></iframe>'
            )
        return "ذخیره کنید تا نمایش داده شود"

    @admin.display(description='Thumbnail Preview')
    def thumbnail_preview(self, obj):
        if obj.aparat_id:
            return format_html(
                '<img src="{}" width="400" style="border-radius: 4px;">',
                obj.thumbnail_url
            )
        return "ذخیره کنید تا نمایش داده شود"

    # تنظیمات اضافی
    save_on_top = True
    show_full_result_count = True
    list_per_page = 25
    date_hierarchy = 'created_at'

    # اکشن اختصاصی
    actions = ['refresh_aparat_ids']

    @admin.action(description='بروزرسانی شناسه آپارات از URLها')
    def refresh_aparat_ids(self, request, queryset):
        updated = 0
        for video in queryset:
            if video.aparat_url:
                new_id = video.extract_video_id(video.aparat_url)
                if new_id and new_id != video.aparat_id:
                    video.aparat_id = new_id
                    video.save()
                    updated += 1
        self.message_user(
            request,
            f"تعداد {updated} شناسه آپارات بروزرسانی شد",
            level='success'
        )






@admin.register(IndustrialTourismImages)
class IndustrialTourismImagesAdmin(admin.ModelAdmin):
    """مدیریت تصاویر گردشگری صنعتی"""
    list_display = ('thumbnail', 'caption', 'industrial_tourism_link', 'created_at')
    list_filter = ('created_at', 'industrial_tourism')
    search_fields = ('caption', 'industrial_tourism__title')
    readonly_fields = ('created_at', 'updated_at', 'image_preview')
    ordering = ('-created_at',)

    fieldsets = (
        (None, {
            'fields': ('industrial_tourism', 'image', 'caption')
        }),
        ('پیش‌نمایش', {
            'fields': ('image_preview',),
            'classes': ('collapse',),
        }),
        ('تاریخچه', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

    def thumbnail(self, obj):
        """نمایش تصویر بندانگشتی در لیست"""
        if obj.image:
            return format_html(
                '<img src="{}" width="50" height="50" style="object-fit: cover; border-radius: 4px;" />',
                obj.image.url
            )
        return "بدون تصویر"

    thumbnail.short_description = "تصویر"

    def industrial_tourism_link(self, obj):
        """لینک به صفحه گردشگری صنعتی مرتبط"""
        url = reverse('admin:articles_industrialtourism_change', args=[obj.industrial_tourism.id])

        return format_html('<a href="{}">{}</a>', url, obj.industrial_tourism.title)

    industrial_tourism_link.short_description = "گردشگری صنعتی"

    def image_preview(self, obj):
        """پیش‌نمایش تصویر در صفحه جزئیات"""
        if obj.image:
            return format_html(
                '<img src="{}" width="100%" style="max-height: 400px; object-fit: contain;" />',
                obj.image.url
            )
        return "بدون تصویر"

    image_preview.short_description = "پیش‌نمایش تصویر"

    def get_queryset(self, request):
        """بهینه‌سازی کوئری با prefetch_related"""
        return super().get_queryset(request).select_related('industrial_tourism')


class IndustrialTourismImagesInline(admin.TabularInline):
    """مدیریت تصاویر به صورت Inline"""
    model = IndustrialTourismImages
    extra = 3
    fields = ('image', 'caption', 'image_preview')
    readonly_fields = ('image_preview',)
    ordering = ('-created_at',)

    def image_preview(self, obj):
        """پیش‌نمایش تصویر در حالت Inline"""
        if obj.image:
            return format_html(
                '<img src="{}" width="100" height="60" style="object-fit: cover; border-radius: 4px;" />',
                obj.image.url
            )
        return "بدون تصویر"

    image_preview.short_description = "پیش‌نمایش"


@admin.register(IndustrialTourism)
class IndustrialTourismAdmin(admin.ModelAdmin):
    """مدیریت گردشگری‌های صنعتی"""
    list_display = ('title', 'base_image_thumbnail', 'video_link', 'images_count', 'created_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('title', 'description')
    readonly_fields = ('created_at', 'updated_at', 'base_image_preview', 'video_preview')
    inlines = [IndustrialTourismImagesInline]
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'

    fieldsets = (
        (None, {
            'fields': ('title', 'description')
        }),
        ('مدیا', {
            'fields': ('base_image', 'base_image_preview', 'video', 'video_preview'),
            'classes': ('collapse',),
        }),
        ('محتوا', {
            'fields': ('content',),
            'classes': ('full-width',),
        }),
        ('تاریخچه', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

    def base_image_thumbnail(self, obj):
        """نمایش تصویر اصلی بندانگشتی در لیست"""
        if obj.base_image:
            return format_html(
                '<img src="{}" width="60" height="40" style="object-fit: cover; border-radius: 4px;" />',
                obj.base_image.url
            )
        return "بدون تصویر"

    base_image_thumbnail.short_description = "تصویر اصلی"

    def video_link(self, obj):
        """نمایش لینک ویدیو در لیست"""
        if obj.video:
            return format_html(
                '<a href="{}" target="_blank" class="button">دانلود ویدیو</a>',
                obj.video.url
            )
        return "بدون ویدیو"

    video_link.short_description = "ویدیو"

    def images_count(self, obj):
        """تعداد تصاویر مرتبط"""
        count = obj.images.count()
        return format_html(
            '<span style="color: {};">{} تصویر</span>',
            'green' if count > 0 else 'red',
            count
        )

    images_count.short_description = "تعداد تصاویر"

    def base_image_preview(self, obj):
        """پیش‌نمایش تصویر اصلی در صفحه جزئیات"""
        if obj.base_image:
            return format_html(
                '<img src="{}" width="100%" style="max-height: 400px; object-fit: contain;" />',
                obj.base_image.url
            )
        return "بدون تصویر"

    base_image_preview.short_description = "پیش‌نمایش تصویر اصلی"

    def video_preview(self, obj):
        """پیش‌نمایش ویدیو در صفحه جزئیات"""
        if obj.video:
            return format_html(
                '<video controls width="100%" style="max-height: 400px;">'
                '<source src="{}" type="video/mp4">'
                'مرورگر شما از تگ ویدیو پشتیبانی نمی‌کند.'
                '</video>',
                obj.video.url
            )
        return "بدون ویدیو"

    video_preview.short_description = "پیش‌نمایش ویدیو"

    def get_queryset(self, request):
        """بهینه‌سازی کوئری با prefetch_related و annotate"""
        return super().get_queryset(request).prefetch_related('images').annotate(
            images_count=Count('images')
        )

    class Media:
        """اضافه کردن استایل‌های سفارشی"""
        css = {
            'all': ('admin/css/custom_admin.css',)
        }
        js = ('admin/js/custom_admin.js',)






