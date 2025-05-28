import json
from .models import Article, Comment
from .serializers import ArticleSerializer, LikeRequestSerializer, RelatedArticleSerializer, CommentSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.exceptions import PermissionDenied
from django.db.models import Q, Count
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.db import connection
from pgvector.django import CosineDistance
from dashboard.models import UserReadArticle
from elasticsearch import Elasticsearch
from rest_framework import generics, permissions
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from datetime import date
from dashboard.models import UserLikedArticle

User = get_user_model()


class ArticleListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            queryset = Article.objects.all()

            category = request.query_params.get('category')
            if category and category != "개체" and category.strip() != "":
                queryset = queryset.filter(category=category)

            sort_by = request.query_params.get('sort_by', 'latest')
            if sort_by == 'recommend':
                queryset = queryset.annotate(like_count=Count('likes')).order_by('-like_count')
            else:
                queryset = queryset.order_by('-write_date')

            page = int(request.query_params.get('page', 1))
            limit = int(request.query_params.get('limit', 10))
            offset = (page - 1) * limit
            total_count = queryset.count()
            total_pages = (total_count + limit - 1) // limit

            articles = queryset[offset:offset+limit]
            serialized = ArticleSerializer(articles, many=True, context={"request": request})

            return Response({
                "message": "호출 성공",
                "data": {
                    "articles": serialized.data,
                    "pagination": {
                        "total_count": total_count,
                        "total_pages": total_pages,
                        "current_page": page,
                        "limit": limit
                    }
                }
            })

        except Exception as e:
            print("ArticleListView 에러:", e)
            return Response({"message": "서버 에러가 발생했습니다."}, status=500)


class SimilarArticleView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, article_id):
        try:
            base_article = Article.objects.get(id=article_id)

            if base_article.embedding is None:
                return Response({"message": "해당 기사에는 임베딩 벡터가 없습니다."}, status=400)

            similar_articles = (
                Article.objects
                .exclude(id=base_article.id)
                .exclude(embedding=None)
                .annotate(distance=CosineDistance("embedding", base_article.embedding))
                .order_by("distance")[:5]
            )

            serialized = ArticleSerializer(similar_articles, many=True, context={"request": request})

            return Response({
                "message": "유사 기사 추천 결과",
                "data": serialized.data
            })

        except Article.DoesNotExist:
            return Response({"message": "해당 기사를 찾을 수 없습니다."}, status=404)
        except Exception as e:
            print("SimilarArticleView 에러:", e)
            return Response({"message": "서버 에러가 발생했습니다."}, status=500)


class ArticleDetailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, pk):
        try:
            print("요청 들어옴:", pk)
            article = get_object_or_404(Article, pk=pk)
            print("기사 불러옴:", article.title)

            serialized = ArticleSerializer(article, context={"request": request})

            if article.embedding is not None:
                similar_articles = (
                    Article.objects
                    .exclude(id=article.id)
                    .exclude(embedding=None)
                    .annotate(distance=CosineDistance("embedding", article.embedding))
                    .order_by("distance")[:5]
                )
                print("관련 기사 개수:", len(similar_articles))

                related_serialized = RelatedArticleSerializer(similar_articles, many=True, context={"request": request})
                related_data = related_serialized.data
            else:
                related_data = []

            return Response({
                "message": "호출 성공",
                "data": {
                    **serialized.data,
                    "related_articles": {
                        "articles": related_data
                    }
                }
            })
        except Exception as e:
            print("🔥 에러 발생:", e)
            return Response({"message": "서버 에러가 발생했습니다.", "detail": str(e)}, status=500)


class LikeToggleView(APIView):
    permission_classes = [IsAuthenticated]  # AllowAny -> IsAuthenticated 로 바꿔야 로그인 유저만 가능

    def get(self, request):
        article_id = request.query_params.get('article_id')
        if not article_id:
            return Response({"message": "article_id가 필요합니다."}, status=400)

        article = get_object_or_404(Article, pk=article_id)
        is_liked = UserLikedArticle.objects.filter(user=request.user, article=article).exists()
        return Response({
            "message": "조회 성공",
            "is_liked": is_liked
        }, status=200)

    def post(self, request):
        user = request.user
        serializer = LikeRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        article = get_object_or_404(Article, pk=serializer.validated_data['article_id'])

        existing = UserLikedArticle.objects.filter(user=user, article=article).first()
        if existing:
            existing.delete()
            liked = False
        else:
            UserLikedArticle.objects.create(user=user, article=article)
            liked = True

        like_count = UserLikedArticle.objects.filter(article=article).count()

        return Response({
            "message": "토글 완료",
            "liked": liked,
            "like_count": like_count,
        }, status=200)

    def delete(self, request):
        serializer = LikeRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        article = get_object_or_404(Article, pk=serializer.validated_data['article_id'])

        UserLikedArticle.objects.filter(user=request.user, article=article).delete()
        return Response({"message": "좋아요 제거됨"}, status=200)


class ReadArticleView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, article_id):
        try:
            article = get_object_or_404(Article, pk=article_id)

            article.read += 1
            article.save(update_fields=["read"])

            user = request.user
            if user.is_authenticated:
                if not UserReadArticle.objects.filter(user=user, article=article, read_at__date=date.today()).exists():
                    UserReadArticle.objects.create(user=user, article=article)

            return Response({
                "read": article.read,
                "like_count": UserLikedArticle.objects.filter(article=article).count(),
                "is_liked": UserLikedArticle.objects.filter(user=user, article=article).exists() if user.is_authenticated else False
            })

        except Article.DoesNotExist:
            return Response({"message": "기사 없음"}, status=404)


class RecommendView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user = request.user
            category = request.query_params.get('category')

            liked_article_ids = UserLikedArticle.objects.filter(
                user=user, article__embedding__isnull=False
            ).values_list("article_id", flat=True)

            liked_articles = Article.objects.filter(id__in=liked_article_ids)

            if not liked_articles.exists():
                return Response({"message": "추천을 위한 데이터가 없습니다."}, status=404)

            import numpy as np
            liked_embeddings = np.array([article.embedding for article in liked_articles])
            user_profile_vector = liked_embeddings.mean(axis=0)

            recommended_queryset = Article.objects.exclude(id__in=liked_article_ids).exclude(embedding=None)

            if category:
                recommended_queryset = recommended_queryset.filter(category=category)

            recommended_articles = (
                recommended_queryset
                .annotate(distance=CosineDistance("embedding", user_profile_vector.tolist()))
                .order_by("distance")[:10]
            )

            results = ArticleSerializer(recommended_articles, many=True, context={"request": request}).data

            return Response({
                "message": "추천 호출 성공",
                "data": {
                    "articles": results,
                    "pagination": {
                        "total_count": len(results),
                        "total_pages": 1,
                        "current_page": 1,
                        "limit": 10
                    }
                }
            }, status=200)

        except Exception as e:
            return Response({"error": str(e)}, status=500)


class LikedArticlesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        liked = UserLikedArticle.objects.filter(user=request.user).select_related('article').order_by('-liked_at')
        articles = [ua.article for ua in liked]
        serializer = ArticleSerializer(articles, many=True, context={"request": request})
        return Response({
            "message": "좋아요한 기사 목록 호출 성공",
            "data": serializer.data
        }, status=200)


class SearchNewsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            query = request.query_params.get("q", "").strip()
            if not query:
                return Response({"message": "검색어를 입력해주세요."}, status=400)

            es = Elasticsearch("http://localhost:9200")
            index_name = "news"

            es_response = es.search(
                index=index_name,
                size=1000,
                query={
                    "bool": {
                        "should": [
                            {"match_phrase": {"title": query}},
                            {"match_phrase": {"content": query}},
                            {"match_phrase": {"writer": query}},
                            {"match_phrase": {"keywords": query}}
                        ],
                        "minimum_should_match": 1
                    }
                }
            )

            print("[검색 결과 수]", len(es_response["hits"]["hits"]))

            # 유사도 기준으로 정렬된 URL 목록
            urls = [hit["_source"]["url"] for hit in es_response["hits"]["hits"]]
            if not urls:
                return Response({"message": "검색 결과가 없습니다.", "data": []})

            page = int(request.query_params.get('page', 1))
            limit = int(request.query_params.get('limit', 1000))
            offset = (page - 1) * limit
            paginated_urls = urls[offset:offset + limit]

            # PostgreSQL에서 URL로 기사 데이터 조회
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT id, title, writer, write_date, category, content, url, keywords
                    FROM news_article
                    WHERE url = ANY(%s)
                """, (paginated_urls,))
                rows = cursor.fetchall()
                columns = [col[0] for col in cursor.description]

            articles = [dict(zip(columns, row)) for row in rows]

            # keywords: JSON 파싱
            for article in articles:
                if isinstance(article["keywords"], str):
                    try:
                        article["keywords"] = json.loads(article["keywords"])
                    except json.JSONDecodeError:
                        article["keywords"] = []

            # Elasticsearch 유사도 순서 유지
            user = request.user if request.user.is_authenticated else None
            article_objs = Article.objects.filter(url__in=paginated_urls)
            url_to_article = {a.url: a for a in article_objs}

            for article in articles:
                obj = url_to_article.get(article["url"])
                if obj:
                    article["article_interaction"] = {
                        "likes": UserLikedArticle.objects.filter(article=obj).count(),
                        "read": obj.read
                    }
                    article["is_liked"] = UserLikedArticle.objects.filter(user=user, article=obj).exists() if user else False
                else:
                    article["article_interaction"] = {"likes": 0, "read": 0}
                    article["is_liked"] = False

            # Elasticsearch 유사도 순서 유지
            url_order = {url: i for i, url in enumerate(paginated_urls)}
            articles.sort(key=lambda x: url_order.get(x["url"], 9999))

            total_count = len(urls)
            total_pages = (total_count + limit - 1) // limit

            return Response({
                "message": "검색 결과입니다",
                "data": {
                    "articles": articles,
                    "pagination": {
                        "total_count": total_count,
                        "total_pages": total_pages,
                        "current_page": page,
                        "limit": limit
                    }
                }
            })

        except Exception as e:
            import traceback
            traceback.print_exc()  # ← 여기에 진짜 문제가 나옴
            return Response({"message": "서버 오류가 발생했습니다.", "detail": str(e)}, status=500)

        
class CommentListCreateAPIView(generics.ListCreateAPIView):
    queryset = Comment.objects.select_related('author').all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        article_id = self.request.query_params.get('article_id')
        return Comment.objects.filter(article_id=article_id).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_update(self, serializer):
        if self.request.user != self.get_object().author:
            raise PermissionDenied("You cannot edit someone else's comment.")
        serializer.save()

    def perform_destroy(self, instance):
        if self.request.user != instance.author:
            raise PermissionDenied("You cannot delete someone else's comment.")
        instance.delete()