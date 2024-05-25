# api/views/view_articles.py
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from articles.models import Article
from api.serializers.serializer_articles import ArticleSerializer

class ArticleList(generics.ListCreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

class ArticleDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    lookup_field = 'slug'  # Use slug instead of pk

@api_view(['GET'])
def latest_article(request):
    try:
        article = Article.objects.latest('created_at')
        serializer = ArticleSerializer(article)
        return Response(serializer.data)
    except Article.DoesNotExist:
        return Response({"error": "No articles found"}, status=404)
