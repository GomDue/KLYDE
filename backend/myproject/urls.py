from django.contrib import admin
from django.urls import include, path
from news.views import ArticleListView

urlpatterns = [
    path("users/", include("users.urls")),
    path('auth/', include('dj_rest_auth.urls')),
    path('auth/registration/', include('dj_rest_auth.registration.urls')),  
    path("admin/", admin.site.urls),
    path("health-check/", include("health_check.urls")), 
    path("news-list/", ArticleListView.as_view()),
    path("news/", include("news.urls")),
    path("chatbot/", include("chat.urls")),
    path("dashboard/", include("dashboard.urls")),
]
