from django.db import models
from django.conf import settings
from news.models import Article
from users.models import User

class UserReadArticle(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    read_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'dashboard_userreadarticle'

    def __str__(self):
        return f"{self.user} read {self.article} on {self.read_at}"

class UserLikedArticle(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    liked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} liked {self.article} on {self.liked_at}"
