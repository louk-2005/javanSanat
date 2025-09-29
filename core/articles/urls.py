# django files
from django.urls import path, include

# rest files
from rest_framework.routers import DefaultRouter

# your files
from .views import (
    ArticleViewSet,
    CategoryViewSet,
    CourseImageViewSet,
    CourseInfoViewSet,
    VideoCastViewSet,
    IndustrialTourismViewSet,
    IndustrialTourismImageViewSet
)

app_name = 'articles'

router = DefaultRouter()
router.register('categories', CategoryViewSet, basename='categories')
router.register('articles', ArticleViewSet, basename='articles')
router.register('course/images', CourseImageViewSet, basename='course-images')
router.register('course/info', CourseInfoViewSet, basename='course-info')
router.register('video', VideoCastViewSet, basename='video-cast')
router.register(r'industrial-tourism', IndustrialTourismViewSet, basename='industrial-tourism')
router.register(r'industrial-tourism-images', IndustrialTourismImageViewSet, basename='industrial-tourism-images')

urlpatterns = [
    path('', include(router.urls)),
]