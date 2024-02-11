from django.urls import path
from .views import (
    AllTasksView,
    CompletedTaskListView,
    TaskExecutionDeleteView,
    TaskDeleteView,
    TaskIndexView,
    TaskCreateView,
    TasksForMeView,
    TaskDetailView,
    TaskExecutionDetailView,
    TaskExecutionUpdateView,
    TaskUpdateView,
    TasksFromMeView,
    TaskExecutionCreateView,
    view_notifications,
)
from . import views

app_name = "tasks"

urlpatterns = [
    path("", TaskIndexView.as_view(), name="index"),
    path("create-task/", TaskCreateView.as_view(), name="create_task"),
    path("<int:pk>/", TaskDetailView.as_view(), name="task_detail"),
    path("update-task/<int:pk>/", TaskUpdateView.as_view(), name="update_task"),
    path("delete-task/<int:pk>/", TaskDeleteView.as_view(), name="delete_task"),
    path("all_tasks/", AllTasksView.as_view(), name="all_tasks"),
    path("from_me_tasks/", TasksFromMeView.as_view(), name="from_me_tasks"),
    path("for_me_tasks/", TasksForMeView.as_view(), name="for_me_tasks"),
    path(
        "task_execution/<int:pk>/",
        TaskExecutionDetailView.as_view(),
        name="task_execution_detail",
    ),
    path(
        "update-task-executon/<int:pk>/",
        TaskExecutionUpdateView.as_view(),
        name="update_task_execution",
    ),
    path(
        "task/<int:task_id>/execution/create/",
        TaskExecutionCreateView.as_view(),
        name="task_execution_create",
    ),
    path(
        "task_execution/<int:pk>/delete/",
        TaskExecutionDeleteView.as_view(),
        name="delete_task_execution",
    ),
    path("view-notifications/", view_notifications, name="view_notifications"),
    path('completed/', CompletedTaskListView.as_view(), name='completed_tasks'),
]
