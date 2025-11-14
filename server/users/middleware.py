"""
Middleware для чтения JWT из cookies и добавления в Authorization header.
DRF ожидает токен в заголовке, но мы храним его в cookie.
"""

class JWTAuthFromCookieMiddleware:
    """
    Middleware для чтения JWT из cookie и добавления в заголовок Authorization.
    DRF ожидает токен в заголовке, но мы храним его в cookie.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Читаем access token из cookie
        access_token = request.COOKIES.get('access_token')

        # Если токен есть, добавляем его в заголовок
        if access_token:
            request.META['HTTP_AUTHORIZATION'] = f'Bearer {access_token}'

        response = self.get_response(request)
        return response