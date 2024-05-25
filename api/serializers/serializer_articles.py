from rest_framework import serializers
from articles.models import Article, ArticleTranslation

class ArticleSerializer(serializers.ModelSerializer):
    image_thumbnail = serializers.ReadOnlyField(source='image_thumbnail.url')
    image_medium = serializers.ReadOnlyField(source='image_medium.url')
    image_large = serializers.ReadOnlyField(source='image_large.url')

    class Meta:
        model = Article
        fields = [
            'id', 'title', 'content', 'author', 'slug',
            'created_at', 'updated_at', 'image_thumbnail',
            'image_medium', 'image_large'
        ]

class ArticleTranslationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleTranslation
        fields = ['id', 'slug', 'title', 'content', 'language', 'article']
