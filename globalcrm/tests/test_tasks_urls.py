from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from tasks.models import Task, TaskExecution

class UrlsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="testuser", password="12345")
        cls.task = Task.objects.create(
            title="Test Task",
            description="This is a test task",
            deadline=timezone.now() + timezone.timedelta(days=1),
            created_by=cls.user,
            worker=cls.user,
        )

    def setUp(self):
        self.client = Client()
        self.client.force_login(self.user)
        self.task_execution = TaskExecution.objects.create(
            title="Test Task Execution",
            task=self.task,
            created_at=timezone.now(),
        )

    def test_index_url(self):
        response = self.client.get(reverse("tasks:index"))
        self.assertIn(response.status_code, [200, 302], msg="tasks:index is not accessible")

    def test_create_task_url(self):
        response = self.client.get(reverse("tasks:create_task"))
        self.assertIn(response.status_code, [200, 302], msg="tasks:create_task is not accessible")

    def test_task_detail_url(self):
        response = self.client.get(reverse("tasks:task_detail", kwargs={"pk": self.task.pk}))
        self.assertIn(response.status_code, [200, 302], msg="tasks:task_detail is not accessible")
    
    def test_task_execution_detail_url(self):
        response = self.client.get(reverse("tasks:task_execution_detail", kwargs={"pk": self.task_execution.pk}))
        self.assertIn(response.status_code, [200, 302], msg="tasks:task_execution_detail is not accessible")

    # def test_urls(self):
    #     urls = [
    #         ("tasks:index", "tasks:index is not accessible"),
    #         ("tasks:create_task", "tasks:create_task is not accessible"),
    #         ("tasks:task_detail", "tasks:task_detail is not accessible"),
    #         ("tasks:update_task", "tasks:update_task is not accessible"),
    #         ("tasks:delete_task", "tasks:delete_task is not accessible"),
    #         ("tasks:all_tasks", "tasks:all_tasks is not accessible"),
    #         ("tasks:from_me_tasks", "tasks:from_me_tasks is not accessible"),
    #         ("tasks:for_me_tasks", "tasks:for_me_tasks is not accessible"),
    #         (
    #             "tasks:task_execution_detail",
    #             "tasks:task_execution_detail is not accessible",
    #         ),
    #         (
    #             "tasks:update_task_execution",
    #             "tasks:update_task_execution is not accessible",
    #         ),
    #         (
    #             "tasks:task_execution_create",
    #             "tasks:task_execution_create is not accessible",
    #         ),
    #         (
    #             "tasks:delete_task_execution",
    #             "tasks:delete_task_execution is not accessible",
    #         ),
    #         ("tasks:view_notifications", "tasks:view_notifications is not accessible"),
    #         ("tasks:completed_tasks", "tasks:completed_tasks is not accessible"),
    #     ]
    #     for url_name, error_message in urls:
    #         if "detail" in url_name or "update" in url_name or "delete" in url_name or "task_execution_create" in url_name:
    #             if "task_execution_create" in url_name:
    #                 response = self.client.get(
    #                     reverse(url_name, kwargs={"task_id": self.task.pk})
    #                 )
    #             else:
    #                 response = self.client.get(
    #                     reverse(url_name, kwargs={"pk": self.task.pk})
    #                 )
    #         elif "task_execution" in url_name:
    #             response = self.client.get(
    #                 reverse(url_name, kwargs={"pk": self.task_execution.pk})
    #             )
    #         else:
    #             response = self.client.get(reverse(url_name))
    #         self.assertIn(response.status_code, [200, 302], msg=error_message)
