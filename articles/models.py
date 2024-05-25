from django.db import models
from tinymce.models import HTMLField
from django.utils.text import slugify
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill


class Article(models.Model):
    title = models.CharField(max_length=200)
    content = HTMLField()
    author = models.CharField(max_length=100)
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='articles/images', blank=True, null=True)

    image_thumbnail = ImageSpecField(source='image',
                                     processors=[ResizeToFill(100, 50)],
                                     format='JPEG',
                                     options={'quality': 60})
    image_medium = ImageSpecField(source='image',
                                  processors=[ResizeToFill(300, 150)],
                                  format='JPEG',
                                  options={'quality': 80})
    image_large = ImageSpecField(source='image',
                                 processors=[ResizeToFill(600, 300)],
                                 format='JPEG',
                                 options={'quality': 90})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)[:255]
            original_slug = self.slug
            counter = 1
            while Article.objects.filter(slug=self.slug).exists():
                self.slug = f"{original_slug}-{counter}"
                if len(self.slug) > 255:
                    self.slug = self.slug[:255 - len(str(counter)) - 1]
                counter += 1
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class ArticleTranslation(models.Model):
    article = models.ForeignKey(Article, related_name='translations', on_delete=models.CASCADE)
    language = models.CharField(max_length=10)
    title = models.CharField(max_length=200)
    content = HTMLField()
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True)

    class Meta:
        unique_together = ('article', 'language')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)[:255]
            original_slug = self.slug
            counter = 1
            while ArticleTranslation.objects.filter(slug=self.slug).exists():
                self.slug = f"{original_slug}-{counter}"
                if len(self.slug) > 255:
                    self.slug = self.slug[:255 - len(str(counter)) - 1]
                counter += 1
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.article.title} ({self.language})"
