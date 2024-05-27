"""
This module defines serializers for the Article and ArticleTranslation models.
"""

from rest_framework import serializers
from articles.models import Article, ArticleTranslation

class ArticleSerializer(serializers.ModelSerializer):
    """
    Serializer class for the Article model.
    """
    image_thumbnail = serializers.ReadOnlyField(source='image_thumbnail.url')
    image_medium = serializers.ReadOnlyField(source='image_medium.url')
    image_large = serializers.ReadOnlyField(source='image_large.url')

    class Meta:
        """
        Meta class to map serializer's fields with the model fields.
        """
        model = Article
        fields = [
            'id', 'title', 'content', 'author', 'slug',
            'created_at', 'updated_at', 'image_thumbnail',
            'image_medium', 'image_large'
        ]

class ArticleTranslationSerializer(serializers.ModelSerializer):
    """
    Serializer class for the ArticleTranslation model.
    """
    class Meta:
        """
        Meta class to map serializer's fields with the model fields.
        """
        model = ArticleTranslation
        fields = ['id', 'slug', 'title', 'content', 'language', 'article']
