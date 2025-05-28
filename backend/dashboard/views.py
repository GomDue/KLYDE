from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from news.models import Article
from dashboard.models import UserReadArticle, UserLikedArticle
from collections import Counter
from datetime import timedelta, date

class DashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        liked_articles_qs = UserLikedArticle.objects.filter(user=user).select_related("article")
        articles = [ula.article for ula in liked_articles_qs]

        # 카테고리 통계
        category_stats = Counter(a.category for a in articles)

        # 키워드 통계
        keyword_stats = Counter(k for a in articles for k in a.keywords)
        keyword_stats = dict(keyword_stats.most_common(5))

        # 날짜별 읽은 기사 수
        week_counter = Counter(
            ura.read_at.date().isoformat()
            for ura in UserReadArticle.objects.filter(
                user=user,
                read_at__date__gte=date.today() - timedelta(days=6)
            )
        )

        # 최근 좋아요한 기사 5개
        recent_favorites = liked_articles_qs.order_by('-liked_at')[:5]
        liked_articles = [
            {
                "id": item.article.id,
                "title": item.article.title,
                "author": item.article.writer,
                "write_date": item.article.write_date.isoformat()
            }
            for item in recent_favorites
        ]

        return Response({
            "category_stats": dict(category_stats),
            "keyword_stats": keyword_stats,
            "read_by_day": dict(week_counter),
            "liked_articles": liked_articles
        })
