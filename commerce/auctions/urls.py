from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("categories", views.categories, name="categories"),
    path("category/<str:category>", views.category, name="category"),
    path("listing/<int:listing_id>", views.listing, name="listing"),
    path("<int:listing_id>/watchlist_operation", views.watchlist_operation, name="watchlist_operation" ),
    path("<int:listing_id>/close", views.close_listing, name="close"),
    path("<int:listing_id>/comment", views.comment, name="comment")
]
