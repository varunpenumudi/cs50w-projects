from django.urls import path
from .import views

urlpatterns = [
    path("", views.index, name="index"),

    # User Auth
    path("register", views.register_view, name="register"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("profile", views.user_profile, name="user_profile"),

    # TASK Views
    path("new", views.new_task, name="new_task"),
    path("delete/<int:id>", views.delete_task, name="delete_task"),
    path("task/<int:id>", views.show_task, name="show_task"),

    # Task Prioritization views
    path("priority-matrix", views.priority_matrix, name="priority_matrix"),
    path("tasks/priority/<int:priority>", views.show_priority_tasks, name="show_priority_tasks"),

    # API Paths
    path("api/tasks", views.api_tasks, name="api_tasks"),
    path("api/tasks/<int:id>", views.api_task, name="api_task"),
    path("api/tasks/priority/<int:priority>", views.api_priority_tasks, name="api_priority_tasks"),
    path("api/subtask/add", views.api_add_subtask, name="api_add_subtask"),
    path("api/subtask/<int:id>", views.api_subtask, name="api_subtask"),
]