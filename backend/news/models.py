from django.db import models
from django.conf import settings
from users.models import User
from pgvector.django import VectorField
from django.utils import timezone

class SafeJSONField(models.JSONField):
    def from_db_value(self, value, expression, connection):
        return value

class Article(models.Model):
    title = models.CharField(max_length=200)
    writer = models.CharField(max_length=255)
    write_date = models.DateTimeField()  
    category = models.CharField(max_length=50)
    content = models.TextField()  
    url = models.URLField(max_length=200, unique=True)
    keywords = SafeJSONField(default=list)
    embedding = VectorField(null=True)
    read = models.IntegerField(default=0) 
    updated_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'news_article'  

class Comment(models.Model):
    article = models.ForeignKey("news.Article", on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey('users.User', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author.email} - {self.content[:20]}"