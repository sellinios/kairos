from rest_framework import serializers
from articles.models import Article, ArticleTranslation

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['id', 'slug', 'title', 'content', 'author', 'image', 'created_at', 'updated_at']

class ArticleTranslationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleTranslation
        fields = ['id', 'slug', 'title', 'content', 'language', 'article']
