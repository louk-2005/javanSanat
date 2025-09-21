# rest files
from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.decorators import action
from rest_framework.response import Response

# django files
from django.shortcuts import get_object_or_404

# your files
from articles.models import Article, Category
from articles.serializers import ArticleSerializer, CategorySerializer


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

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAdminUser()]
