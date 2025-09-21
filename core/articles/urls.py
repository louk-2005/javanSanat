# django files
from django.urls import path, include

# rest files
from rest_framework.routers import DefaultRouter

# your files
from .views import ArticleViewSet, CategoryViewSet

app_name = 'articles'

router = DefaultRouter()
router.register('categories', CategoryViewSet, basename='categories')
router.register('articles', ArticleViewSet, basename='articles')

urlpatterns = [
    path('', include(router.urls)),
]