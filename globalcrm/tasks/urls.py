from django.urls import path
from .views import (DeleteTaskView,
                    IndexView,
                    CreateTaskView, MyTasks,
                    TaskDetailView, TaskExecutionDetailView,
                    UpdateTaskView,
                    FromMeTasks,
                    TaskExecutionCreateView)
from . import views

app_name = 'tasks'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('create-task/', CreateTaskView.as_view(), name='create_task'),
    path('<int:pk>/', TaskDetailView.as_view(), name='task_detail'),
    path('update-task/<int:pk>/', UpdateTaskView.as_view(), name='update_task'),
    path('delete-task/<int:pk>/', DeleteTaskView.as_view(), name='delete_task'),
    path('from_me_tasks/', FromMeTasks.as_view(), name='from_me_tasks'),
    path('my_tasks/', MyTasks.as_view(), name='my_tasks'),
    path('task_execution/create/', TaskExecutionCreateView.as_view(), name='task_execution_create'),
    path('task_execution/<int:pk>/', TaskExecutionDetailView.as_view(), name='task_execution_detail'),
]
