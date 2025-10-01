# rest files
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from urllib.parse import urlparse

#your files
from .models import Category, Article, CourseInfo, CourseImage, VideoCast, IndustrialTourism, IndustrialTourismImages

from accounts.models import User


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'created_at']
        read_only_fields = ['slug', 'created_at']


class UserMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name']


class ArticleSerializer(serializers.ModelSerializer):
    author = UserMinimalSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    featured_image_url = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = [
            'id', 'title', 'slug', 'excerpt', 'content', 'featured_image',
            'featured_image_url', 'created_at', 'updated_at', 'author', 'category','show'
        ]
        read_only_fields = ['slug', 'created_at', 'updated_at']

    def get_featured_image_url(self, obj):
        if obj.featured_image:
            return self.context['request'].build_absolute_uri(obj.featured_image.url)
        return None

    def create(self, validated_data):
        # Set author to current authenticated user
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)











class CourseImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseImage
        fields = ['id', 'caption', 'image', 'created_at', 'course']
        read_only_fields = ['id', 'created_at']


class CourseInfoSerializer(serializers.ModelSerializer):
    images = CourseImageSerializer(many=True, read_only=True)  # فقط نمایش
    final_price = serializers.DecimalField(
        max_digits=11, decimal_places=2, read_only=True
    )
    price_display = serializers.SerializerMethodField()
    duration_display = serializers.SerializerMethodField()

    class Meta:
        model = CourseInfo
        fields = [
            'id', 'title', 'slug', 'description', 'base_image',
            'teachers', 'start_date', 'end_date', 'duration',
            'duration_display', 'price', 'discount', 'final_price',
            'price_display', 'is_published', 'images',
            'created_at', 'updated_at',
        ]
        read_only_fields = ['slug', 'created_at', 'updated_at', 'final_price']

    def get_price_display(self, obj):
        """نمایش قیمت با فرمت مناسب"""
        return f"{obj.final_price:,.0f} تومان" if obj.final_price else "رایگان"

    def get_duration_display(self, obj):
        """نمایش مدت زمان دوره به ساعت و دقیقه"""
        if obj.duration:
            hours = obj.duration // 60
            minutes = obj.duration % 60
            return f"{hours} ساعت و {minutes} دقیقه" if minutes else f"{hours} ساعت"
        return None


class CourseInfoWriteSerializer(serializers.ModelSerializer):
    """
    سریالایزر برای ایجاد/ویرایش دوره همراه با آپلود تصاویر
    """
    images = CourseImageSerializer(many=True, required=False)

    class Meta:
        model = CourseInfo
        fields = [
            'id', 'title', 'slug', 'description', 'base_image',
            'teachers', 'start_date', 'end_date', 'duration',
            'price', 'discount', 'is_published', 'images'
        ]
        read_only_fields = ['slug']

    def create(self, validated_data):
        images_data = validated_data.pop('images', [])
        course = CourseInfo.objects.create(**validated_data)
        for image_data in images_data:
            CourseImage.objects.create(course=course, **image_data)
        return course

    def update(self, instance, validated_data):
        images_data = validated_data.pop('images', [])
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        for image_data in images_data:
            CourseImage.objects.create(course=instance, **image_data)

        return instance








class VideoCastSerializer(serializers.ModelSerializer):
    embed_url = serializers.ReadOnlyField()
    thumbnail_url = serializers.ReadOnlyField()

    class Meta:
        model = VideoCast
        fields = [
            "id", "title", "aparat_url", "aparat_id",
            "order", "created_at", "updated_at",
            "embed_url", "thumbnail_url",
        ]
        read_only_fields = ("aparat_id", "created_at", "updated_at")

    def validate_aparat_url(self, value):
        """اعتبارسنجی لینک آپارات و استخراج شناسه ویدیو"""
        if not value:
            raise ValidationError("لینک آپارات الزامی است")

        video_id = self.extract_video_id(value)
        if not video_id:
            raise ValidationError("لینک آپارات نامعتبر است. لطفاً لینک صحیح وارد کنید")

        # بررسی تکراری نبودن شناسه
        qs = VideoCast.objects.filter(aparat_id=video_id)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise ValidationError("این ویدیو قبلاً ثبت شده است")

        return value

    def create(self, validated_data):
        """ایجاد نمونه جدید با استخراج شناسه ویدیو"""
        validated_data["aparat_id"] = self.extract_video_id(validated_data["aparat_url"])
        return super().create(validated_data)

    def update(self, instance, validated_data):
        """به‌روزرسانی شناسه در صورت تغییر لینک"""
        new_url = validated_data.get("aparat_url")
        if new_url and new_url != instance.aparat_url:
            validated_data["aparat_id"] = self.extract_video_id(new_url)
        return super().update(instance, validated_data)

    @staticmethod
    def extract_video_id(url: str) -> str | None:
        """استخراج شناسه ویدیو از لینک آپارات"""
        try:
            parsed = urlparse(url)
            path_parts = parsed.path.strip("/").split("/")

            if "aparat.com" not in parsed.netloc:
                return None

            # حالت معمولی: /v/VIDEO_ID
            if len(path_parts) >= 2 and path_parts[0] in ["v", "video"]:
                return path_parts[1]

            # حالت embed: /videohash/VIDEO_ID/...
            if "videohash" in path_parts:
                idx = path_parts.index("videohash") + 1
                return path_parts[idx] if idx < len(path_parts) else None
        except Exception:
            return None
        return None





class IndustrialTourismImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = IndustrialTourismImages
        fields = [
            "id",
            "caption",
            "image",
            "image_url",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ("created_at", "updated_at")

    def get_image_url(self, obj):
        request = self.context.get("request")
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return obj.image.url if obj.image else None


class IndustrialTourismSerializer(serializers.ModelSerializer):
    base_image_url = serializers.SerializerMethodField()
    video_url = serializers.SerializerMethodField()
    images = IndustrialTourismImageSerializer(many=True, read_only=True)

    class Meta:
        model = IndustrialTourism
        fields = [
            "id",
            "title",
            "base_image",
            "base_image_url",
            "video",
            "video_url",
            "description",
            "content",
            "images",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ("created_at", "updated_at")

    def get_base_image_url(self, obj):
        request = self.context.get("request")
        if obj.base_image and request:
            return request.build_absolute_uri(obj.base_image.url)
        return obj.base_image.url if obj.base_image else None

    def get_video_url(self, obj):
        request = self.context.get("request")
        if obj.video and request:
            return request.build_absolute_uri(obj.video.url)
        return obj.video.url if obj.video else None