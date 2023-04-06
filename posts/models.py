from django.db import models
from django.utils.translation import gettext_lazy


class Post(models.Model):
    class MessageType(models.TextChoices):
        ANNOUNCEMENT = "Announcement", gettext_lazy("Announcement")
        QOTW = "QOTW", gettext_lazy("Question of the week")
        USER_CONTENT = "User Content", gettext_lazy("User Content")

    owner = models.ForeignKey(
        "core.DiscordUser",
        related_name="posts",
        on_delete=models.CASCADE)

    id = models.CharField(primary_key=True, max_length=10)

    title = models.CharField(max_length=255)
    content = models.TextField(blank=True, null=True)
    file_url = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    message_type = models.CharField(
        max_length=12,
        choices=MessageType.choices,
        default=None)

    reddit_url = models.CharField(blank=True, null=True, max_length=100)

    class Meta:
        ordering = ("title",)
        verbose_name_plural = "Posts"

    def __str__(self):
        return self.title
