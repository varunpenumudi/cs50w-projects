from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    following = models.ManyToManyField("self", related_name="followers", symmetrical=False, blank=True)
    pass

# ToDo: 
# Create Models to represent posts, likes, and followers

class Post(models.Model):
    poster = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    content = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    liked_users = models.ManyToManyField(User, related_name="liked_posts", blank=True)

    def __str__(self) -> str:
        return f"{self.content} posted by {self.poster}"

    def serialize(self):
        return {
            "id": self.id,
            "poster": self.poster.username,
            "content": self.content,
            "timestamp": self.date_created,
            "likes": self.liked_users.count(),
        }