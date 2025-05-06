from http import HTTPStatus

from django.utils import timezone
from drf_spectacular.utils import (
    OpenApiExample,
    extend_schema,
)
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from rest_framework import serializers, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import exception_handler

from project.restful.serializers import LoginAuthSerializer, RegisterAuthSerializer


def api_exception_handler(exc, context):
    # Call DRF's default exception handler first
    response = exception_handler(exc, context)

    if response is not None:
        # Standardize the error response format

        if isinstance(exc, ValidationError):
            detail = exc.detail
        else:
            detail = response.data.get("detail") or "An error occured"

        error_payload = {
            "error": {
                "message": HTTPStatus(response.status_code).description,
                "detail": detail,
                "code": getattr(exc, "code", None) or response.status_code,
            },
            "meta": {"timestamp": timezone.now()},
        }
        response.data = error_payload

    return response


class AuthenticationViewSet(viewsets.GenericViewSet):

    authentication_classes = []

    @extend_schema(
        summary="Register",
    )
    @action(detail=False, url_path="sign-up", methods=["POST"])
    def sign_up(self, request):
        """The register endpoint allows new users to create an account by submitting the required
        registration information. Upon successful validation, a new user record is created in the
        system, and the endpoint returns the newly registered user’s details. This endpoint may also
        trigger additional processes, such as sending a confirmation email. It is typically used
        as the entry point for user onboarding in applications that require user accounts."""

        serializer = RegisterAuthSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @extend_schema(
        summary="Login",
        examples=[
            OpenApiExample(
                "Login success example",
                value={
                    "data": {"access_token": "3qjP3Euld5j6MmNylpcP6AZFyrpGwZAEX6IV_vmGqF4"},
                    "meta": {"timestamp": "2019-08-24T14:15:22Z"},
                },
                response_only=True,
                status_codes=[200],
            )
        ],
    )
    @action(detail=False, url_path="sign-in", methods=["POST"])
    def sign_in(self, request):
        """The login endpoint allows users to authenticate by submitting their login credentials.
        Upon successful authentication, the endpoint returns a JSON Web Token (JWT) that the client
        can use to authorize subsequent requests. If the credentials are invalid, the endpoint
        responds with an appropriate error message. This endpoint is a critical part of
        the authentication flow and is designed to securely validate user identities before
        granting access to protected resources."""

        serializer = LoginAuthSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_authenticate_header(self, request):
        return "Bearer"

    def get_serializer_class(self):
        if self.action == "sign_up":
            return RegisterAuthSerializer
        elif self.action == "sign_in":
            return LoginAuthSerializer
        return serializers.Serializer  # fallback


class PublicSchemaView(SpectacularAPIView):
    authentication_classes = []
    permission_classes = [AllowAny]


class PublicRedocView(SpectacularRedocView):
    authentication_classes = []
    permission_classes = [AllowAny]


class PublicSwaggerView(SpectacularSwaggerView):
    authentication_classes = []
    permission_classes = [AllowAny]
