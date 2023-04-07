"""
URL configuration for TransPlaceSite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, include
from core.views import index, resources, discord_login, discord_login_redirect, logout_view
from posts.views import content_overview, content_detail, content_all
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets


urlpatterns = [
    path("", index, name="index"),
    path("about/", index, name="index"),
    path("resources/", resources, name="resources"),
    path("posts/", content_overview, name="posts"),
    path("posts/list/<str:pk>/", content_all, name="view_all"),
    path("posts/details/<str:pk>/", content_detail, name="details"),

    path("auth/login/", discord_login, name="login"),
    path("auth/login/redirect/", discord_login_redirect, name="login_redirect"),
    path("logout/", logout_view, name="logout"),

    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("api/", include("posts.urls"), name="api"),

    path("admin/", admin.site.urls),
]
