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
    authentication_classes = [] # НЕ ПРИМЕНЯТЬ JWT-аутентификацию к этому view
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get('refresh_token')
        if not refresh_token:
            return Response(
                {'error': 'Refresh token not found in cookies'},
                status=status.HTTP_400_BAD_REQUEST
            )

        request.data['refresh'] = refresh_token
        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:
            new_access_token = response.data.get('access')
            new_refresh_token = response.data.get('refresh')

            # Определяем, нужно ли "помнить" пользователя, на основе cookie
            remember_me = request.COOKIES.get('auth_remember_me') == 'True'
            refresh_max_age = 30 * 24 * 60 * 60 if remember_me else 7 * 24 * 60 * 60

            if new_access_token:
                response.set_cookie(
                    key='access_token', value=new_access_token,
                    httponly=True, secure=True, samesite='Lax', max_age=900
                )
            
            if new_refresh_token:
                response.set_cookie(
                    key='refresh_token', value=new_refresh_token,
                    httponly=True, secure=True, samesite='Lax', max_age=refresh_max_age
                )
                # Продлеваем жизнь и для remember_me cookie
                response.set_cookie(
                    key='auth_remember_me', value=str(remember_me),
                    httponly=True, secure=True, samesite='Lax', max_age=refresh_max_age
                )

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
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')
        response.delete_cookie('auth_remember_me') # Удаляем и remember_me
        return response


class LoginView(generics.GenericAPIView):
    """
    Аутентификация пользователя.
    Доступно для всех (AllowAny).
    """
    authentication_classes = []  # НЕ ПРИМЕНЯТЬ JWT-аутентификацию к этому view
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        remember_me = request.data.get('remember_me', False)

        user = authenticate(username=username, password=password)
        if user is None:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)
        refresh_max_age = 30 * 24 * 60 * 60 if remember_me else 7 * 24 * 60 * 60
        
        if remember_me:
            refresh.set_exp(lifetime=timedelta(days=30))

        response = Response({'user': UserSerializer(user).data}, status=status.HTTP_200_OK)

        response.set_cookie(
            key='access_token', value=str(refresh.access_token),
            httponly=True, secure=True, samesite='Lax', max_age=900
        )
        response.set_cookie(
            key='refresh_token', value=str(refresh),
            httponly=True, secure=True, samesite='Lax', max_age=refresh_max_age
        )
        response.set_cookie(
            key='auth_remember_me', value=str(remember_me),
            httponly=True, secure=True, samesite='Lax', max_age=refresh_max_age
        )

        return response


class RegisterView(generics.CreateAPIView):
    """
    Регистрация нового пользователя.
    Доступно для всех (AllowAny).
    """
    authentication_classes = []  # НЕ ПРИМЕНЯТЬ JWT-аутентификацию к этому view
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        remember_me = request.data.get('remember_me', False)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        refresh = RefreshToken.for_user(user)
        refresh_max_age = 30 * 24 * 60 * 60 if remember_me else 7 * 24 * 60 * 60

        if remember_me:
            refresh.set_exp(lifetime=timedelta(days=30))
        
        response = Response({'user': UserSerializer(user).data}, status=status.HTTP_201_CREATED)

        response.set_cookie(
            key='access_token', value=str(refresh.access_token),
            httponly=True, secure=True, samesite='Lax', max_age=900
        )
        response.set_cookie(
            key='refresh_token', value=str(refresh),
            httponly=True, secure=True, samesite='Lax', max_age=refresh_max_age
        )
        response.set_cookie(
            key='auth_remember_me', value=str(remember_me),
            httponly=True, secure=True, samesite='Lax', max_age=refresh_max_age
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
