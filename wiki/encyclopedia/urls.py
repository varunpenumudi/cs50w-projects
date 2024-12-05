from django.urls import path

from . import views

app_name="encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entry_name>", views.show_entry, name="entry"),
    path("create/", views.create_entry, name="create"),
    path("edit/<str:entry_name>", views.edit_entry, name="edit"),
    path("random/",views.random, name="random"),
]