# django files
from django.db import models
from django.utils.text import slugify
from django_resized import ResizedImageField
# your packages
from django_ckeditor_5.fields import CKEditor5Field

# your files
from accounts.models import User


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, allow_unicode=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "دسته‌بندی"
        verbose_name_plural = "دسته‌بندی‌ها"
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)


class Article(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)
    excerpt = models.TextField(max_length=500, blank=True)
    content = CKEditor5Field(config_name='default')
    featured_image = ResizedImageField(
        size=[1900, 1000],                  # سایز خروجی (عرض × ارتفاع)
        crop=['middle', 'center'],        # کراپ از کجا انجام بشه (اختیاری)
        quality=75,                       # کیفیت (0 تا 100)
        upload_to='article_images/',            # مسیر ذخیره‌سازی
        force_format='WEBP',               # تبدیل فرمت (jpg, png, webp و غیره)
        blank=True, null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='articles')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='articles')

    class Meta:
        verbose_name = "مقاله"
        verbose_name_plural = "مقالات"
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)


