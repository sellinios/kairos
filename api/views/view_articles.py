from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from articles.models import Article, ArticleTranslation
from api.serializers.serializer_articles import ArticleSerializer

class ArticleList(generics.ListCreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    def get_queryset(self):
        language = self.request.query_params.get('language', 'en')
        articles = Article.objects.prefetch_related('translations')
        translated_articles = []

        for article in articles:
            translation = article.translations.filter(language=language).first()
            if translation:
                translated_articles.append({
                    'id': article.id,
                    'slug': translation.slug,
                    'title': translation.title,
                    'content': translation.content,
                    'author': article.author,
                    'image_thumbnail': article.image_thumbnail.url if article.image else None,
                    'image_medium': article.image_medium.url if article.image else None,
                    'image_large': article.image_large.url if article.image else None,
                    'created_at': article.created_at,
                    'updated_at': article.updated_at
                })
            else:
                translated_articles.append({
                    'id': article.id,
                    'slug': article.slug,
                    'title': article.title,
                    'content': article.content,
                    'author': article.author,
                    'image_thumbnail': article.image_thumbnail.url if article.image else None,
                    'image_medium': article.image_medium.url if article.image else None,
                    'image_large': article.image_large.url if article.image else None,
                    'created_at': article.created_at,
                    'updated_at': article.updated_at
                })
        return translated_articles

class ArticleDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    lookup_field = 'slug'

    def get_object(self):
        language = self.request.query_params.get('language', 'en')
        obj = super().get_object()
        translation = obj.translations.filter(language=language).first()
        if translation:
            obj.slug = translation.slug
            obj.title = translation.title
            obj.content = translation.content
        return obj

@api_view(['GET'])
def latest_articles(request):
    language = request.query_params.get('language', 'en')
    articles = Article.objects.order_by('-created_at')[:5].prefetch_related('translations')
    response_data = []

    for article in articles:
        translation = article.translations.filter(language=language).first()
        if translation:
            response_data.append({
                'id': article.id,
                'slug': translation.slug,
                'title': translation.title,
                'content': translation.content,
                'author': article.author,
                'image_thumbnail': article.image_thumbnail.url if article.image else None,
                'image_medium': article.image_medium.url if article.image else None,
                'image_large': article.image_large.url if article.image else None,
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
                'image_thumbnail': article.image_thumbnail.url if article.image else None,
                'image_medium': article.image_medium.url if article.image else None,
                'image_large': article.image_large.url if article.image else None,
                'created_at': article.created_at,
                'updated_at': article.updated_at
            })
    return Response(response_data)
