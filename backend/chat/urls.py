from django.urls import path
from .views import ChatQAView

urlpatterns = [
    path("", ChatQAView.as_view(), name="chatbot"),
]
