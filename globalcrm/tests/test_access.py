from django.test import TestCase
from django.urls import reverse


class AccessTest(TestCase):
    def test_unauthenticated_user_access(self):
        create_task_url = reverse("tasks:create_task")
        create_task_response = self.client.get(create_task_url)
        self.assertEqual(create_task_response.status_code, 302,
                         "Неаутентифицированные пользователи должны быть перенаправлены на страницу входа при доступе к странице создания задачи")

        tasks_list_url = reverse("tasks:index")
        tasks_list_response = self.client.get(tasks_list_url)
        self.assertEqual(tasks_list_response.status_code, 302,
                         "Неаутентифицированные пользователи должны быть перенаправлены на страницу входа при доступе к списку задач")