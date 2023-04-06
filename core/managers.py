from django.contrib.auth import models


class DiscordOAuth2Manager(models.UserManager):
    def create_new_discord_user(self, user):
        print("HI")
        new_user = self.create(
            id=user["id"],
            avatar=user["avatar"],
            public_flags=user["public_flags"],
            username=user["username"],
            is_verified=user["is_verified"]
        )
        return new_user


