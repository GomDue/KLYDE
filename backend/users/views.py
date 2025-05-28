from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer
from rest_framework import status


class AuthUserInfoView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)
    
    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)


class LoginAPIView(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        user = authenticate(email=email, password=password)

        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "user_id": user.id,
                "email": user.email
            })
        else:
            return Response({"detail": "아이디 또는 비밀번호가 올바르지 않습니다."}, status=400)
        
        
class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        current_password = request.data.get("current_password")
        new_password = request.data.get("new_password")

        if not current_password or not new_password:
            return Response({"detail": "비밀번호를 모두 입력해주세요."}, status=400)

        if not user.check_password(current_password):
            return Response({"detail": "현재 비밀번호가 올바르지 않습니다."}, status=400)

        if current_password == new_password:
            return Response({"detail": "새 비밀번호가 기존과 동일합니다."}, status=400)

        user.set_password(new_password)
        user.save()
        return Response({"message": "비밀번호가 성공적으로 변경되었습니다."}, status=200)


class DeleteAccountView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        user = request.user
        user.delete()
        return Response({"message": "계정이 삭제되었습니다."}, status=200)
    

class EmailConsentUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        user = request.user
        consent = request.data.get("email_consent")

        if isinstance(consent, bool):
            user.email_consent = consent
            user.save()
            return Response({"message": "Email consent updated."}, status=200)
        return Response({"detail": "Invalid value for email_consent."}, status=400)