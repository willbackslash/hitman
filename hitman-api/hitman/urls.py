"""hitman URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.routers import SimpleRouter
from rest_framework.authtoken import views

from hitman import settings
from hits.viewsets.hits_viewset import HitViewSet
from users.viewsets.user_viewset import UserViewSet

schema_view = get_schema_view(
    openapi.Info(
        title="Hitman API",
        default_version="v1",
        description="Test description",
        contact=openapi.Contact(email="macwilliamdlc@gmail.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

swagger_urls = [
    url(
        r"^spec(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    url(
        r"^docs/$",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    url(
        r"^redoc/$", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"
    ),
]

router = SimpleRouter(trailing_slash=False)
router.register("users", UserViewSet, basename="users")
router.register("hits", HitViewSet, basename="hits")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    url(r"^api/auth/token", views.obtain_auth_token),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += swagger_urls
