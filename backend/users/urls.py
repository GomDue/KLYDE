from django.urls import path
from .views import AuthUserInfoView, LoginAPIView, ChangePasswordView, DeleteAccountView, EmailConsentUpdateView

urlpatterns = [
    path("user/", AuthUserInfoView.as_view()),
    path("login/", LoginAPIView.as_view()),
    path("change-password/", ChangePasswordView.as_view(), name="change-password"),
    path("delete-account/", DeleteAccountView.as_view(), name="delete-account"),
    path('email-consent/', EmailConsentUpdateView.as_view()),
]
