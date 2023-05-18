from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.core.cache import cache
from rest_framework import generics, permissions

from core.models import DiscordUser
from .serializers import PostSerializer, UserSerializer
from .models import Post
from .permissions import IsOwnerOrReadOnly
from reddit.utils import get_messages

from timeit import default_timer as timer


@login_required(login_url="/auth/login/")
def content_overview(request: HttpRequest):
    if not request.user.is_verified:
        return render(request, "posts/need-verification.html")

    start = timer()

    fetch_start = timer()

    posts = cache.get("posts")
    print(cache)

    if not posts:
        print("Fetching latest reddit content")
        posts = get_messages()

    fetch_end = timer()

    fancy_start = timer()
    # Creates the cool column effect (when screen is large enough)
    content = [[], []]
    # content = [content[:len(content) // 2], content[len(content) // 2:]]
    for i in range(0, (len(posts) - 1) // 2, 2):
        content[0].append(posts[i])
        content[1].append(posts[i + 1])

    fancy_end = timer()

    end = timer()

    print(f"overall time {end-start}",
          f"fetch time: {fetch_end-fetch_start}",
          f"fancy stuff time: {fancy_end-fancy_start}"
          )

    return render(request, "posts/view_all.html", {
        "content": content,
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