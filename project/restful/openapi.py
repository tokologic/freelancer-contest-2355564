from drf_spectacular.openapi import AutoSchema
from drf_spectacular.plumbing import get_class
from drf_spectacular.utils import extend_schema_serializer
from rest_framework import serializers


def enveloper(serializer_class, many, pagination_class=None):
    from rest_framework.settings import api_settings

    component_name = "Enveloped{}{}".format(
        serializer_class.__name__.replace("Serializer", ""),
        "List" if many else "",
    )

    if not pagination_class:
        pagination_class = api_settings.DEFAULT_PAGINATION_CLASS

    class MetaSerializer(serializers.Serializer):
        timestamp = serializers.DateTimeField()

    @extend_schema_serializer(many, component_name=component_name)
    class EnvelopeSerializer(serializers.Serializer):
        data = serializer_class(many=many)
        meta = MetaSerializer()

        def __init__(self, instance=None, data=..., **kwargs):
            super().__init__(instance, data, **kwargs)

    return EnvelopeSerializer


class ProjectAutoSchema(AutoSchema):
    def get_response_serializers(self):
        """use envelope on all default responses. @extend_schema will override this change"""
        serializer_class = get_class(self._get_serializer())
        many = self._is_list_view(serializer_class)
        if many:
            return self._get_serializer()
        else:
            return enveloper(
                serializer_class=serializer_class,
                many=self._is_list_view(serializer_class),
            )
