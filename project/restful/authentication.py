# from rest_framework import authentication
from rest_framework import exceptions
from rest_framework_simplejwt import authentication


class JWTAuthentication(authentication.JWTAuthentication):
    def authenticate(self, request):

        result = super().authenticate(request)
        if result is None:
            raise exceptions.AuthenticationFailed("Need valid authentication mechanism")

        return result

    def authenticate_header(self, request):
        return "Bearer"
