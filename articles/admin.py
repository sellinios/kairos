# articles/admin.py
from django.contrib import admin
from .models import Article
from tinymce.widgets import TinyMCE
from django.db import models
from modeltranslation.admin import TranslationAdmin

class ArticleAdmin(TranslationAdmin):
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE()},
    }
    list_display = ('title', 'author', 'created_at', 'updated_at')
    search_fields = ('title', 'author')
    list_filter = ('created_at', 'updated_at')

admin.site.register(Article, ArticleAdmin)
