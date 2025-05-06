from django.utils import timezone
from rest_framework.renderers import JSONRenderer


class ApiRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        status_code = renderer_context["response"].status_code
        if 200 <= status_code <= 299:

            if data and "data" not in data:
                data = {"data": data, "meta": {"timestamp": timezone.now()}}

        return super().render(data, accepted_media_type, renderer_context)
