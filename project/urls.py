"""
URL configuration for the project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import include, path
from rest_framework import routers

from project.restful.views import (
    AuthenticationViewSet,
    PublicRedocView,
    PublicSchemaView,
    PublicSwaggerView,
)
from project.vehicle.views import VehicleViewSet

apiRouter = routers.DefaultRouter()
apiRouter.register(r"vehicles", VehicleViewSet)
apiRouter.register("auth", AuthenticationViewSet, basename="auth")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("_docs_/_schema_/", PublicSchemaView.as_view(), name="schema"),
    path("_docs_/_api_documentation_/", PublicRedocView.as_view(), name="redoc_schema"),
    path("_docs_/_try_it_/", PublicSwaggerView.as_view(), name="swagger_schema"),
    path("", include(apiRouter.urls)),
]
