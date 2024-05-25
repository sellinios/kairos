from rest_framework import serializers
from articles.models import Article

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['id', 'slug', 'title', 'content', 'author', 'created_at', 'updated_at', 'image']  # Include image
