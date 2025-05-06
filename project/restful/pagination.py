from django.conf import settings
from django.utils import timezone
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class ApiPageNumberPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 1000

    def get_paginated_response(self, data):
        link_key = settings.HATEOAS["LINK_KEY"]

        return Response(
            {
                "data": data,
                "meta": {
                    "timestamp": timezone.now(),
                    "pagination": {
                        "total": self.page.paginator.count,
                        "current_page": self.page.number,
                        "total_pages": self.page.paginator.num_pages,
                        "page_size": self.page_size,
                        "count": len(data),
                        link_key: {
                            "next": self.get_next_link(),
                            "previous": self.get_previous_link(),
                        },
                    },
                },
            }
        )

    def get_paginated_response_schema(self, schema):
        link_key = settings.HATEOAS["LINK_KEY"]

        return {
            "type": "object",
            "properties": {
                "data": schema,
                "meta": {
                    "type": "object",
                    "properties": {
                        "pagination": {
                            "type": "object",
                            "properties": {
                                "total": {
                                    "type": "integer",
                                    "example": 100,
                                },
                                "current_page": {
                                    "type": "integer",
                                    "example": 3,
                                },
                                "total_pages": {
                                    "type": "integer",
                                    "example": 20,
                                },
                                "page_size": {
                                    "type": "integer",
                                    "example": 10,
                                },
                                "count": {
                                    "type": "integer",
                                    "example": 10,
                                },
                                link_key: {
                                    "type": "object",
                                    "properties": {
                                        "next": {
                                            "type": "string",
                                            "nullable": True,
                                            "format": "uri",
                                            "example": "http://example.com/vehicles/?{page_query_param}=4".format(  # noqa: B950
                                                page_query_param=self.page_query_param
                                            ),
                                        },
                                        "previous": {
                                            "type": "string",
                                            "nullable": True,
                                            "format": "uri",
                                            "example": "http://example.com/vehicles/?{page_query_param}=2".format(  # noqa: B950
                                                page_query_param=self.page_query_param
                                            ),
                                        },
                                    },
                                },
                            },
                        },
                        "timestamp": {"type": "string", "format": "date-time"},
                    },
                },
            },
        }
