from rest_framework.decorators import api_view
from rest_framework.response import Response
from articles.models import Article, ArticleTranslation
from api.serializers.serializer_articles import ArticleSerializer

@api_view(['GET'])
def latest_articles(request):
    language = request.query_params.get('language', 'en')
    try:
        articles = Article.objects.order_by('-created_at')[:5]
        response_data = []
        for article in articles:
            translation = ArticleTranslation.objects.filter(article=article, language=language).first()
            if translation:
                response_data.append({
                    'id': article.id,
                    'slug': translation.slug,
                    'title': translation.title,
                    'content': translation.content,
                    'author': article.author,
                    'image': article.image.url if article.image else None,
                    'created_at': article.created_at,
                    'updated_at': article.updated_at
                })
            else:
                response_data.append({
                    'id': article.id,
                    'slug': article.slug,
                    'title': article.title,
                    'content': article.content,
                    'author': article.author,
                    'image': article.image.url if article.image else None,
                    'created_at': article.created_at,
                    'updated_at': article.updated_at
                })
        return Response(response_data)
    except Article.DoesNotExist:
        return Response({"error": "No articles found"}, status=404)
