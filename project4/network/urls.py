
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    # Post views
    path("posts/create", views.create_post, name="create_post"),
    path("posts/update/<int:post_id>", views.update_post, name="update_post"),
    path("posts/like/<int:post_id>", views.like_post, name="like_post"),

    # Following tab view
    path("following", views.following, name="following"),

    #User Profile
    path("profile/<str:username>", views.user_profile, name="user_profile"),

    # Follow/Unfollow a user
    path("follow/<str:username>", views.follow, name="follow"),
    path("unfollow/<str:username>", views.unfollow, name="unfollow"),
]
