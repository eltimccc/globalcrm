from django.urls import path
from .views import (
    AllTasks,
    DeleteTaskExecutionView,
    DeleteTaskView,
    IndexView,
    CreateTaskView,
    ForMeTasks,
    TaskDetailView,
    TaskExecutionDetailView,
    UpdateTaskExecution,
    UpdateTaskView,
    FromMeTasks,
    TaskExecutionCreateView,
)
from . import views

app_name = "tasks"

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("create-task/", CreateTaskView.as_view(), name="create_task"),
    path("<int:pk>/", TaskDetailView.as_view(), name="task_detail"),
    path("update-task/<int:pk>/", UpdateTaskView.as_view(), name="update_task"),
    path("delete-task/<int:pk>/", DeleteTaskView.as_view(), name="delete_task"),
    path("all_tasks/", AllTasks.as_view(), name="all_tasks"),
    path("from_me_tasks/", FromMeTasks.as_view(), name="from_me_tasks"),
    path("for_me_tasks/", ForMeTasks.as_view(), name="for_me_tasks"),
    path(
        "task_execution/create/",
        TaskExecutionCreateView.as_view(),
        name="task_execution_create",
    ),
    path(
        "task_execution/<int:pk>/",
        TaskExecutionDetailView.as_view(),
        name="task_execution_detail",
    ),
    path(
        "update-task-executon/<int:pk>/",
        UpdateTaskExecution.as_view(),
        name="update_task_execution",
    ),
    path(
        "task/<int:task_id>/execution/create/",
        TaskExecutionCreateView.as_view(),
        name="task_execution_create",
    ),
    path(
        "task_execution/<int:pk>/delete/",
        DeleteTaskExecutionView.as_view(),
        name="delete_task_execution",
    ),
]
