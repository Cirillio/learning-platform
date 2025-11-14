from rest_framework import generics, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView
from django.contrib.auth import get_user_model, authenticate
from datetime import timedelta

from .serializers import (
    UserRegistrationSerializer,
    UserSerializer,
    UserProfileSerializer,
)
from .models import UserProfile

User = get_user_model()


class RefreshTokenView(TokenRefreshView):
    """
    Обновление access токена с использованием refresh токена из куки.
    Доступно для всех (AllowAny), но требует валидный refresh токен.
    """
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        # Получаем refresh_token из куки
        refresh_token = request.COOKIES.get('refresh_token')
        if not refresh_token:
            return Response(
                {'error': 'Refresh token not found in cookies'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Устанавливаем токен в request.data для стандартной обработки
        request.data['refresh'] = refresh_token

        # Вызываем родительский метод
        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:
            # Обновляем куки с новым access_token
            new_access_token = response.data.get('access')
            if new_access_token:
                response.set_cookie(
                    key='access_token',
                    value=new_access_token,
                    httponly=True,
                    secure=True,
                    samesite='Lax',
                    max_age=900  # 15 минут
                )
                # Удаляем access и refresh из JSON ответа, так как они в куках
                response.data.pop('access', None)
                response.data.pop('refresh', None)

        return response
    

class LogoutView(generics.GenericAPIView):
    """
    Выход пользователя.
    Удаляет access и refresh токены из куки.
    Доступно только авторизованным пользователям.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        response = Response({'detail': 'Successfully logged out.'}, status=status.HTTP_200_OK)

        # Удаляем куки с токенами
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')

        return response


class LoginView(generics.GenericAPIView):
    """
    Аутентификация пользователя.
    Доступно для всех (AllowAny).
    """
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        remember_me = request.data.get('remember_me', False)  # Флаг "запомнить меня"

        if not username or not password:
            return Response(
                {'error': 'Username and password are required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = authenticate(username=username, password=password)

        if user is None:
            return Response(
                {'error': 'Invalid credentials'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        # Генерируем JWT токены
        refresh = RefreshToken.for_user(user)

        # Устанавливаем время жизни в зависимости от remember_me
        if remember_me:
            # 30 дней для refresh токена
            refresh.set_exp(lifetime=timedelta(days=30))
        # access токен всегда 15 минут (из настроек)

        response = Response({
            'user': UserSerializer(user).data,
        }, status=status.HTTP_200_OK)

        response.set_cookie(            
            key='access_token',
            value=str(refresh.access_token),
            httponly=True,
            secure=True,
            samesite='Lax',
            max_age=900  # 15 минут
        )

        # max_age для refresh токена: 30 дней если remember_me, иначе 7 дней
        refresh_max_age = 30 * 24 * 60 * 60 if remember_me else 7 * 24 * 60 * 60

        response.set_cookie(
            key='refresh_token',
            value=str(refresh),
            httponly=True,
            secure=True,
            samesite='Lax',
            max_age=refresh_max_age
        )

        return response


class RegisterView(generics.CreateAPIView):
    """
    Регистрация нового пользователя.
    Доступно для всех (AllowAny).
    """
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        remember_me = request.data.get('remember_me', False)  # Флаг "запомнить меня"
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Генерируем JWT токены
        refresh = RefreshToken.for_user(user)
        
        response = Response({
            'user': UserSerializer(user).data,
        }, status=status.HTTP_201_CREATED)

        # Устанавливаем время жизни в зависимости от remember_me
        if remember_me:
            # 30 дней для refresh токена
            refresh.set_exp(lifetime=timedelta(days=30))

        response.set_cookie(            
            key='access_token',
            value=str(refresh.access_token),
            httponly=True,
            secure=True,
            samesite='Lax',
            max_age=900
        )

        # max_age для refresh токена: 30 дней если remember_me, иначе 7 дней
        refresh_max_age = 30 * 24 * 60 * 60 if remember_me else 7 * 24 * 60 * 60

        response.set_cookie(
            key='refresh_token',
            value=str(refresh),
            httponly=True,
            secure=True,
            samesite='Lax',
            max_age=refresh_max_age
        )

        return response


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
