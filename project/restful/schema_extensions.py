from drf_spectacular.extensions import (
    OpenApiAuthenticationExtension,
    OpenApiSerializerExtension,
)
from drf_spectacular.plumbing import force_instance


class JWTAuthenticationScheme(OpenApiAuthenticationExtension):
    target_class = "project.restful.authentication.JWTAuthentication"
    name = "JWTAuthentication"

    def get_security_definition(self, auto_schema):
        return {
            "type": "http",
            "scheme": "Bearer",
            "bearerFormat": "JWT",
        }


class PaginationWrapperExtension(OpenApiSerializerExtension):
    target_class = "project.restful.serializers.PaginationWrapper"

    def get_name(self, auto_schema, direction):
        return auto_schema.get_paginated_name(
            auto_schema._get_serializer_name(
                serializer=force_instance(self.target.serializer_class),
                direction=direction,
            )
        )

    def map_serializer(self, auto_schema, direction):
        component = auto_schema.resolve_serializer(self.target.serializer_class, direction)
        paginated_schema = self.target.pagination_class().get_paginated_response_schema(
            component.ref
        )
        return paginated_schema
