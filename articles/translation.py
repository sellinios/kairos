# articles/translation.py
from modeltranslation.translator import register, TranslationOptions
from .models import Article

@register(Article)
class ArticleTranslationOptions(TranslationOptions):
    fields = ('title', 'content', 'author')  # Include all fields that should be translated