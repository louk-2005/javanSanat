# django files
from django.db import models
from django.utils.text import slugify
from django_resized import ResizedImageField
# your packages
from django_ckeditor_5.fields import CKEditor5Field
from django.utils.text import slugify
from urllib.parse import urlparse, parse_qs
# your files
from accounts.models import User


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="نام")
    slug = models.SlugField(max_length=100, unique=True, allow_unicode=True, verbose_name="اسلاگ")
    description = models.TextField(blank=True, verbose_name="توضیحات")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")

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
    title = models.CharField(max_length=200, verbose_name="عنوان")
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True, verbose_name="اسلاگ")
    excerpt = models.TextField(max_length=500, blank=True, verbose_name="خلاصه")
    content = CKEditor5Field(config_name='default', verbose_name="محتوا")
    featured_image = ResizedImageField(
        size=[1900, 1000],  # سایز خروجی (عرض × ارتفاع)
        quality=75,  # کیفیت (0 تا 100)
        upload_to='article_images/',  # مسیر ذخیره‌سازی
        force_format='WEBP',  # تبدیل فرمت (jpg, png, webp و غیره)
        blank=True, null=True,
        verbose_name="تصویر اصلی"
    )
    show = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ بروزرسانی")

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='articles', verbose_name="نویسنده")
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='articles', verbose_name="دسته بندی")

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


class CourseInfo(models.Model):
    title = models.CharField(max_length=200, verbose_name="عنوان"
                                                          "")
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True, verbose_name="اسلاگ")
    description = CKEditor5Field(config_name='default', verbose_name="توضیحات")
    base_image = ResizedImageField(
        size=[1900, 1000],  # سایز خروجی (عرض × ارتفاع)
        quality=75,  # کیفیت (0 تا 100)
        upload_to='course/base_images',  # مسیر ذخیره‌سازی
        force_format='WEBP',  # تبدیل فرمت (jpg, png, webp و غیره)
        blank=True, null=True,
        verbose_name="تصویر اصلی"
    )
    teachers = models.CharField(max_length=300, blank=True, null=True, verbose_name="نام اساتید")
    start_date = models.DateField(blank=True, null=True, verbose_name="تاریخ شروغ")
    end_date = models.DateField(blank=True, null=True, verbose_name="تاریخ پایان")
    duration = models.PositiveIntegerField(help_text="مدت زمان دوره به دقیقه", null=True, blank=True,
                                           verbose_name="مدت زمان")

    price = models.DecimalField(max_digits=11, decimal_places=2, verbose_name="قیمت")
    discount = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True, verbose_name="تخفیف")

    is_published = models.BooleanField(default=False, verbose_name="منتشر شود")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ بروزرسانی")

    class Meta:
        verbose_name = "دروه"
        verbose_name_plural = "دوره های آموزشی"
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    @property
    def final_price(self):
        if self.price is None:
            return None
        if self.discount:
            return self.price - self.discount
        return self.price

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)


class CourseImage(models.Model):
    caption = models.CharField(
        max_length=300,
        blank=True,
        null=True,
        verbose_name="توضیح تصویر"
    )

    image = ResizedImageField(
        size=[1900, 1000],  # سایز خروجی (عرض × ارتفاع)
        quality=75,  # کیفیت (0 تا 100)
        upload_to='course/course_images/',  # مسیر ذخیره‌سازی
        force_format='WEBP',  # تبدیل فرمت (jpg, png, webp و غیره)
        verbose_name="تصویر"
    )

    course = models.ForeignKey(
        "CourseInfo",
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name="دوره"
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="تاریخ ایجاد"
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="تاریخ بروزرسانی"
    )

    def __str__(self):
        return self.caption or f"تصویر #{self.id} - {self.course.title}"

    class Meta:
        verbose_name = "تصویر"
        verbose_name_plural = "تصاویر دوره‌ها"
        ordering = ['-created_at']


class VideoCast(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name="عنوان ویدیو",
        help_text="مثلاً: جلسه اول - معرفی دوره"
    )
    aparat_url = models.URLField(
        verbose_name="لینک آپارات",
        help_text="لینک کامل ویدیو از آپارات را وارد کنید",
    )
    aparat_id = models.CharField(
        max_length=50,
        editable=False,
        unique=True,
        verbose_name="شناسه ویدیو",
        help_text="به صورت خودکار از لینک استخراج می‌شود"
    )

    order = models.PositiveIntegerField(
        default=1,
        verbose_name="ترتیب نمایش"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="تاریخ ایجاد"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="آخرین ویرایش"
    )

    class Meta:
        verbose_name = "ویدیوی آپارات"
        verbose_name_plural = "ویدیوهای آپارات"
        ordering = ["order", "created_at"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.aparat_url:
            new_id = self.extract_video_id(self.aparat_url)
            if new_id and new_id != self.aparat_id:
                self.aparat_id = new_id
        super().save(*args, **kwargs)

    @staticmethod
    def extract_video_id(url: str) -> str | None:
        """
        استخراج Video ID از لینک‌های آپارات
        پشتیبانی: aparat.com/v/..., aparat.com/video/video/embed/videohash/...
        """
        parsed = urlparse(url)
        path_parts = parsed.path.strip("/").split("/")
        if "aparat.com" in parsed.netloc:
            if len(path_parts) >= 2 and path_parts[0] in ["v", "video"]:
                # حالت معمولی: /v/VIDEO_ID
                return path_parts[1]
            elif "videohash" in path_parts:
                # حالت embed: /video/video/embed/videohash/VIDEO_ID/vt/frame
                idx = path_parts.index("videohash") + 1
                return path_parts[idx] if idx < len(path_parts) else None
        return None

    @property
    def embed_url(self):
        """لینک embeddable برای iframe آپارات"""
        return f"https://www.aparat.com/video/video/embed/videohash/{self.aparat_id}/vt/frame"

    @property
    def thumbnail_url(self):
        """
        متأسفانه آپارات مثل یوتیوب لینک مستقیم thumbnail ثابت نداره.
        ساده‌ترین راه: استفاده از API آپارات (در صورت نیاز).
        اینجا فقط یک placeholder می‌ذاریم.
        """
        return f"https://aparat.com/static/thumbs/{self.aparat_id}.jpg"


class IndustrialTourism(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name="عنوان"
    )

    base_image = ResizedImageField(
        size=[1900, 1000],
        quality=75,
        upload_to='IndustrialTourism/base_images',
        force_format='WEBP',
        blank=True, null=True,
        verbose_name="تصویر اصلی"
    )

    video = models.FileField(
        upload_to='IndustrialTourism/videos',
        blank=True, null=True,
        verbose_name="ویدیو"
    )
    description = models.TextField(verbose_name="توضیحات")
    content = CKEditor5Field(
        config_name='default',
        verbose_name="محتوا"
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="تاریخ ایجاد"
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="تاریخ بروزرسانی"
    )

    class Meta:
        verbose_name = "گردشگری صنعتی"
        verbose_name_plural = "گردشگری‌های صنعتی"
        ordering = ["created_at"]

    def __str__(self):
        return self.title


class IndustrialTourismImages(models.Model):
    caption = models.CharField(
        max_length=300,
        blank=True,
        null=True,
        verbose_name="توضیح تصویر"
    )

    image = ResizedImageField(
        size=[1900, 1000],  # سایز خروجی (عرض × ارتفاع)
        quality=75,  # کیفیت (0 تا 100)
        upload_to='IndustrialTourism/images',  # مسیر ذخیره‌سازی
        force_format='WEBP',  # تبدیل فرمت (jpg, png, webp و غیره)
        verbose_name="تصویر"
    )

    industrial_tourism = models.ForeignKey(
        "IndustrialTourism",
        on_delete=models.CASCADE,
        related_name="images",
        verbose_name="گردشگری صنعتی"
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="تاریخ ایجاد"
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="تاریخ بروزرسانی"
    )

    def __str__(self):
        return self.caption or f"تصویر #{self.id} - {self.IndustrialTourism.title}"

    class Meta:
        verbose_name = "تصویر"
        verbose_name_plural = "تصاویر گردشگری صنعتی"
        ordering = ['-created_at']
