# rest files
from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend


# django files
from django.shortcuts import get_object_or_404

# your files
from articles.models import (
    Article,
    Category,
    CourseImage,
    CourseInfo,
    VideoCast,
    IndustrialTourism,
    IndustrialTourismImages
)
from articles.serializers import (
    ArticleSerializer,
    CategorySerializer,
    CourseImageSerializer,
    CourseInfoSerializer,
    CourseInfoWriteSerializer,
    VideoCastSerializer,
    IndustrialTourismImages,
    IndustrialTourismImageSerializer, IndustrialTourismSerializer
)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    @action(detail=True, methods=['GET'])
    def articles(self, request, pk=None):
        category = self.get_object()
        articles = Article.objects.filter(category=category)
        serializer = ArticleSerializer(articles, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'articles']:
            return [AllowAny()]
        return [IsAdminUser()]


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('show',)

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAdminUser()]


class CourseImageViewSet(viewsets.ModelViewSet):
    queryset = CourseImage.objects.all()
    serializer_class = CourseImageSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAdminUser()]


class CourseInfoViewSet(viewsets.ModelViewSet):
    queryset = CourseInfo.objects.all()

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return CourseInfoSerializer
        return CourseInfoWriteSerializer

    @action(detail=True, methods=['GET'])
    def course_images(self, request, pk=None):
        course = self.get_object()
        images = CourseImage.objects.filter(course=course)
        serializer = CourseImageSerializer(images, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAdminUser()]





class VideoCastViewSet(viewsets.ModelViewSet):
    """
    ویو ست کامل برای مدیریت ویدیوهای آپارات
    - لیست، ایجاد، مشاهده، ویرایش و حذف ویدیوها
    - پشتیبانی از فیلتر، جستجو و مرتب‌سازی
    """
    queryset = VideoCast.objects.all()
    serializer_class = VideoCastSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['order']
    search_fields = ['title']
    ordering_fields = ['order', 'created_at', 'updated_at']
    ordering = ['order', 'created_at']

    def get_queryset(self):
        """
        سفارشی‌سازی کوئری با پشتیبانی از:
        - فیلتر بر اساس ترتیب نمایش
        - جستجو در عنوان ویدیو
        """
        queryset = super().get_queryset()

        # فیلتر بر اساس ترتیب نمایش
        order = self.request.query_params.get('order')
        if order:
            queryset = queryset.filter(order=order)

        return queryset

    def perform_create(self, serializer):
        """
        افزودن اطلاعات کاربر هنگام ایجاد ویدیو
        """
        serializer.save()

    @action(detail=True, methods=['get'])
    def embed_info(self, request, pk=None):
        """
        دریافت اطلاعات اضافی برای embed کردن ویدیو
        - لینک embed
        - آدرس تصویر بندانگشتی
        """
        video = self.get_object()
        data = {
            'embed_url': video.embed_url,
            'thumbnail_url': video.thumbnail_url,
            'title': video.title
        }
        return Response(data)

    @action(detail=False, methods=['get'])
    def recent(self, request):
        """
        دریافت 5 ویدیوی اخیر
        """
        recent_videos = VideoCast.objects.order_by('-created_at')[:5]
        serializer = self.get_serializer(recent_videos, many=True)
        return Response(serializer.data)





class IndustrialTourismViewSet(viewsets.ModelViewSet):
    """
    ویوست برای مدیریت گردشگری صنعتی
    شامل: لیست، جزئیات، ایجاد، ویرایش و حذف
    """
    queryset = IndustrialTourism.objects.all().prefetch_related("images")
    serializer_class = IndustrialTourismSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'articles']:
            return [AllowAny()]
        return [IsAdminUser()]


class IndustrialTourismImageViewSet(viewsets.ModelViewSet):
    """
    ویوست برای مدیریت تصاویر گردشگری صنعتی
    """
    queryset = IndustrialTourismImages.objects.all().select_related("industrial_tourism")
    serializer_class = IndustrialTourismImageSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'articles']:
            return [AllowAny()]
        return [IsAdminUser()]











