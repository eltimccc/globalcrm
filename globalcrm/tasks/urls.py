from django.urls import path
from .views import (DeleteTaskView,
                    IndexView,
                    CreateTaskView,
                    TaskDetailView,
                    UpdateTaskView)

app_name = 'tasks'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('create-task/', CreateTaskView.as_view(), name='create_task'),
    path('<int:pk>/', TaskDetailView.as_view(), name='task_detail'),
    path('update-task/<int:pk>/', UpdateTaskView.as_view(), name='update_task'),
    path('delete-task/<int:pk>/', DeleteTaskView.as_view(), name='delete_task'),
]
