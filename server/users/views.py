from rest_framework import generics, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model

from .serializers import (
    UserRegistrationSerializer,
    UserSerializer,
    UserProfileSerializer,
)
from .models import UserProfile

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    """
    Регистрация нового пользователя.
    Доступно для всех (AllowAny).
    """
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Генерируем JWT токены
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'user': UserSerializer(user).data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)


class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    Получение и обновление профиля текущего пользователя.
    Доступно только авторизованным пользователям.
    """
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # Возвращаем профиль текущего пользователя
        profile, created = UserProfile.objects.get_or_create(user=self.request.user)
        return profile


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet для просмотра списка пользователей.
    Только для чтения (list, retrieve).
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        """
        Получить информацию о текущем пользователе.
        GET /api/users/me/
        """
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
