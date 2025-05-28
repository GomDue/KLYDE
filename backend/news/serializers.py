from rest_framework import serializers
from .models import Article, Comment
from dashboard.models import UserLikedArticle


class ArticleSerializer(serializers.ModelSerializer):
    article_interaction = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = [
            'id', 'title', 'content', 'write_date', 'category', 'writer',
            'url', 'article_interaction', 'is_liked'
        ]

    def get_article_interaction(self, obj):
        return {
            "likes": UserLikedArticle.objects.filter(article=obj).count(),
            "read": obj.read
        }

    def get_is_liked(self, obj):
        user = self.context.get('request').user
        if not user.is_authenticated:
            return False
        return UserLikedArticle.objects.filter(user=user, article=obj).exists()



class LikeRequestSerializer(serializers.Serializer):
    article_id = serializers.IntegerField()


class RelatedArticleSerializer(serializers.ModelSerializer):
    article_interaction = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = ['id', 'title', 'write_date', 'article_interaction']

    def get_article_interaction(self, obj):
        return {
            "likes": UserLikedArticle.objects.filter(article=obj).count(),
            "read": obj.read
        }
    
class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'article', 'author', 'content', 'created_at']
        read_only_fields = ['author', 'created_at']

    def get_author(self, obj):
        return obj.author.email
