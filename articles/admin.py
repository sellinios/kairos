from django.contrib import admin
from .models import Article, ArticleTranslation
from tinymce.widgets import TinyMCE
from django.db import models

class ArticleTranslationInline(admin.TabularInline):
    model = ArticleTranslation
    extra = 1
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE()},
    }

class ArticleAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE()},
    }
    list_display = ('title', 'author', 'created_at', 'updated_at')
    search_fields = ('title', 'author')
    list_filter = ('created_at', 'updated_at')
    inlines = [ArticleTranslationInline]
    prepopulated_fields = {'slug': ('title',)}  # Optional: Only if you want to allow manual slug editing

admin.site.register(Article, ArticleAdmin)
