from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from rest_framework import generics, permissions

from core.models import DiscordUser
from .serializers import PostSerializer, UserSerializer
from .models import Post
from .permissions import IsOwnerOrReadOnly


@login_required(login_url="/auth/login/")
def content_overview(request: HttpRequest):
    if not request.user.is_verified:
        return render(request, "posts/need-verification.html")

    user_content = Post.objects.filter(message_type="User Content")[0:5]
    server_messages = Post.objects.exclude(message_type="User Content")[0:3]

    return render(request, "posts/overview.html", {
        "user_content": user_content,
        "server_messages": server_messages
    })


@login_required(login_url="/auth/login/")
def content_detail(request, pk):
    if not request.user.is_verified:
        return render(request, "posts/need-verification.html")

    # It returns a list-like object, so only take the first item
    post = Post.objects.filter(id=pk)[0]

    return render(request, "posts/details.html", {
        "post": post
    })


class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]


    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        IsOwnerOrReadOnly,
    ]


class UserList(generics.ListAPIView):
    queryset = DiscordUser.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = DiscordUser.objects.all()
    serializer_class = UserSerializer
