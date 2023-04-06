from rest_framework import serializers
from .models import Post
from core.models import DiscordUser


class PostSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")

    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "content",
            "file_url",
            "message_type",
            "reddit_url",
            "owner",
        ]


class UserSerializer(serializers.ModelSerializer):
    posts = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Post.objects.all())

    class Meta:
        model = DiscordUser
        fields = ["id", "username", "posts"]
