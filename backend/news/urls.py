from django.urls import path
from .views import *

urlpatterns = [
    path('', ArticleListView.as_view(), name='article_list'),
    path('<int:pk>/', ArticleDetailView.as_view(), name='article_detail'),
    # path('search/', ArticleSearchView.as_view(), name='article_search'),
    path('like/', LikeToggleView.as_view(), name='article_like_toggle'),
    path('<int:article_id>/read/', ReadArticleView.as_view(), name='article_increment_read'),
    path('recommend/', RecommendView.as_view(), name='article_recommend'),
    path('liked/', LikedArticlesView.as_view(), name='liked_articles'),
    path("similar/<int:article_id>/", SimilarArticleView.as_view(), name="similar-articles"),
    path("search/", SearchNewsView.as_view(), name="news_search"),
    path('comments/', CommentListCreateAPIView.as_view(), name='comment-list-create'),
    path('comments/<int:pk>/', CommentDetailAPIView.as_view(), name='comment-detail'),
]
