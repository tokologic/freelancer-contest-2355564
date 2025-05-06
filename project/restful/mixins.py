from django.conf import settings
from rest_framework.fields import empty
from rest_framework.reverse import reverse

from project.restful.serializers import LinkSerializer, LinkSerializerObject


class HATEOASMixin:
    def __init__(self, instance=None, data=empty, **kwargs):
        super().__init__(instance, data, **kwargs)

        self.link_key = settings.HATEOAS["LINK_KEY"]

        if self.link_key not in self.fields:
            self.fields[self.link_key] = LinkSerializer(read_only=True)

    def to_representation(self, instance):
        setattr(
            instance,
            self.link_key,
            LinkSerializerObject(
                {
                    "self": self._get_self_link(instance),
                    "related": self.get_related_link(instance),
                }
            ),
        )
        return super().to_representation(instance)

    def _get_self_link(self, instance):
        resource_name = instance.__class__.__name__.lower()
        return self._reverse(f"{resource_name}-detail", kwargs={"pk": instance.id})

    def _reverse(self, alias, kwargs=None):
        request = self.context.get("request")

        return reverse(alias, request=request, kwargs=kwargs)

    def get_related_link(self, instance):
        return {}
