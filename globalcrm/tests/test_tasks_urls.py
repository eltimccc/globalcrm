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
        self.assertIn(response.status_code, [200], msg="tasks:index is not accessible")

    def test_create_task_url(self):
        response = self.client.get(reverse("tasks:create_task"))
        self.assertIn(response.status_code, [200], msg="tasks:create_task is not accessible")

    def test_task_detail_url(self):
        response = self.client.get(reverse("tasks:task_detail", kwargs={"pk": self.task.pk}))
        self.assertIn(response.status_code, [200], msg="tasks:task_detail is not accessible")
    
    def test_update_task_accessibility(self):
        response = self.client.get(reverse("tasks:update_task", kwargs={"pk": self.task.pk}))
        self.assertIn(response.status_code, [200], msg="tasks:update_task is not accessible")

    def test_delete_task_accessibility(self):
        response = self.client.get(reverse("tasks:delete_task", kwargs={"pk": self.task.pk}))
        self.assertIn(response.status_code, [200], msg="tasks:delete_task is not accessible")

    def test_all_tasks_accessibility(self):
        response = self.client.get(reverse("tasks:all_tasks"))
        self.assertIn(response.status_code, [200], msg="tasks:all_tasks is not accessible")

    def test_from_me_tasks_accessibility(self):
        response = self.client.get(reverse("tasks:from_me_tasks"))
        self.assertIn(response.status_code, [200], msg="tasks:from_me_tasks is not accessible")

    def test_for_me_tasks_accessibility(self):
        response = self.client.get(reverse("tasks:for_me_tasks"))
        self.assertIn(response.status_code, [200], msg="tasks:for_me_tasks is not accessible")

    def test_task_execution_detail_url(self):
        response = self.client.get(reverse("tasks:task_execution_detail", kwargs={"pk": self.task_execution.pk}))
        self.assertIn(response.status_code, [200], msg="tasks:task_execution_detail is not accessible")

    def test_update_task_execution_accessibility(self):
        response = self.client.get(reverse("tasks:update_task_execution", kwargs={"pk": self.task_execution.pk}))
        self.assertIn(response.status_code, [200], msg="tasks:update_task_execution is not accessible")

    def test_task_execution_create_accessibility(self):
        response = self.client.get(reverse("tasks:task_execution_create", kwargs={"task_id": self.task.id}))
        self.assertIn(response.status_code, [200], msg="tasks:task_execution_create is not accessible")

    def test_delete_task_execution_accessibility(self):
        response = self.client.get(reverse("tasks:delete_task_execution", kwargs={"pk": self.task_execution.pk}))
        self.assertIn(response.status_code, [200], msg="tasks:delete_task_execution is not accessible")

    def test_view_notifications_accessibility(self):
        response = self.client.get(reverse("tasks:view_notifications"))
        self.assertIn(response.status_code, [200], msg="tasks:view_notifications is not accessible")

    def test_completed_tasks_accessibility(self):
        response = self.client.get(reverse("tasks:completed_tasks"))
        self.assertIn(response.status_code, [200], msg="tasks:completed_tasks is not accessible")
