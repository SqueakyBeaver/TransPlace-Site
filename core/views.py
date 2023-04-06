from django.shortcuts import render, redirect
from django.http import HttpRequest, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models.query import QuerySet
from .managers import DiscordOAuth2Manager
from .models import DiscordUser

from dotenv import load_dotenv
from os import getenv
import requests

# Might need to change later
API_ENDPOINT = 'https://discord.com/api/v10'

load_dotenv()


def index(request: HttpRequest):
    print(request.user)
    print(request.session.items())
    return render(request, "core/index.html")


def resources(request: HttpRequest):
    return render(request, "core/resources.html")


@login_required(login_url="/auth/login/")
def logout_view(request: HttpRequest):
    if request.user.is_authenticated:
        logout(request)
        return redirect("index")


def discord_login(request: HttpRequest):
    return redirect(getenv("DISCORD_OAUTH2_URL"))


def discord_login_redirect(request: HttpRequest):
    code = request.GET.get('code')
    user = exchange_code(code)

    # if cancelled auth, go back home
    if user is None:
        return redirect("index")

    discord_user: DiscordUser = authenticate(request, user=user)
    print(type(discord_user))
    print(discord_user.backend)
    print(discord_user)

    login(request, user=discord_user)
    print(request.user)
    return redirect("index")


def exchange_code(code: str):
    data = {
        "client_id": getenv("OAUTH_ID"),
        "client_secret": getenv("OAUTH_SECRET"),
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": getenv("REDIRECT_URI"),
        "scope": "identiy guild"
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",

    }
    response = requests.post(
        f"{API_ENDPOINT}/oauth2/token",
        data=data,
        headers=headers)

    response.raise_for_status()
    print(response)
    credentials = response.json()

    # if cancelled auth
    if "error" in list(credentials.keys()):
        return None

    access_token = credentials["access_token"]

    response = requests.get(
        f"{API_ENDPOINT}/users/@me/guilds/959551566388547676/member",
        headers={
            "Authorization": f"Bearer {access_token}",
        })

    member_info = response.json()
    print(member_info)

    if not response.ok:
        response = requests.get(
            f"{API_ENDPOINT}/users/@me",
            headers={
                "Authorization": f"Bearer {access_token}",
            })
        member_info = response.json()
        print(response)
        print(member_info)

        user_info = {
            "id": member_info["id"],
            "avatar": member_info["avatar"],
            "public_flags": member_info["public_flags"],
            "username": f"{member_info['username']}#{member_info['discriminator']}",
            "is_verified": False}

        return user_info

    user_info = {
        "id": member_info["user"]["id"],
        "avatar": member_info["user"]["avatar"],
        "public_flags": member_info["user"]["public_flags"],
        "username": f"{member_info['user']['username']}#{member_info['user']['discriminator']}",
        "is_verified": '959748411844874240' in member_info["roles"]}

    return user_info
