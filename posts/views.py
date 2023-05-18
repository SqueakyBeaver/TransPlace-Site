from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.core.cache import cache

from core.models import DiscordUser
from reddit.utils import get_messages


@login_required(login_url="/auth/login/")
def content_overview(request: HttpRequest):
    if not request.user.is_verified:
        return render(request, "posts/need-verification.html")

    posts = cache.get("posts")
    print(cache)

    if not posts:
        print("Fetching latest reddit content")
        posts = get_messages()

    return render(request, "posts/view_all.html", {
        "posts": posts,
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
