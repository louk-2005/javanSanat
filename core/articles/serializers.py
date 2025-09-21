# serializers.py
from rest_framework import serializers
from .models import Category, Article
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
            'featured_image_url', 'created_at', 'updated_at', 'author', 'category'
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