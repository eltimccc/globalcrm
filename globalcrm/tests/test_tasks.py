from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.utils import timezone
from tasks.models import Task, TaskExecution
from tasks.views import TaskUpdateView, TaskDeleteView
from django.core.exceptions import ValidationError, PermissionDenied
from django.contrib.messages.storage.fallback import FallbackStorage


class TaskModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username="testuser", password="12345")
        cls.task = Task.objects.create(
            title="Test Task",
            description="This is a test task",
            deadline=timezone.now() + timezone.timedelta(days=1),
            created_by=cls.user,
            worker=cls.user,
        )
        cls.execution = TaskExecution.objects.create(
            title="Test Execution",
            description="This is a test execution",
            deadline=timezone.now() + timezone.timedelta(days=1),
            task=cls.task,
        )

    def test_task_creation(self):
        task_data = {
            "title": "Test Task",
            "description": "This is a test task",
            "deadline": timezone.now() + timezone.timedelta(days=1),
            "created_by": self.user,
            "worker": self.user,
        }
        task = Task.objects.create(**task_data)

        for field, value in task_data.items():
            self.assertEqual(getattr(task, field), value, f"Неверное значение поля {field}")

        self.assertFalse(task.completed, "Задача помечена как завершенная")

    def test_task_completion(self):
        self.task.completed = True
        self.task.save()

        self.assertTrue(self.task.completed, "Задача не была помечена как завершенная")
        self.assertIsNotNone(self.task.completed_at, "Поле completed_at не было заполнено")

    def test_task_execution_creation(self):
        execution_data = {
            "title": "Test Execution",
            "description": "This is a test execution",
            "deadline": timezone.now() + timezone.timedelta(days=1),
            "task": self.task,
        }

        execution = TaskExecution.objects.create(**execution_data)

        for field, value in execution_data.items():
            self.assertEqual(getattr(execution, field), value, f"Неверное значение поля {field}")

    def test_deadline_cannot_be_set_before_today(self):
        yesterday = timezone.now() - timezone.timedelta(days=1)

        with self.assertRaisesMessage(
            ValidationError,
            "Дата выполнения не может быть установлена на прошедшую дату!",
        ):
            Task.objects.create(
                title="Test Task",
                description="This is a test task",
                deadline=yesterday,
                created_by=self.user,
                worker=self.user,
            ).full_clean()


class SignalTest(TestCase):
    def setUp(self):
        self.task_creator = User.objects.create_user(username="task_creator", password="12345")
        self.task_worker = User.objects.create_user(username="task_worker", password="12345")
        self.unauthorized_user = User.objects.create_user(username="unauthorized_user", password="12345")

    def test_task_completion_signal(self):
        task = Task.objects.create(
            title="Test Task",
            description="This is a test task",
            deadline=timezone.now() + timezone.timedelta(days=1),
            created_by=self.task_creator,
            worker=self.task_worker,
        )

        task.completed = True
        task.save()
        self.assertIsNotNone(
            task.completed_at, "Дата завершения задачи не была установлена"
        )

        task.completed = False
        task.save()
        self.assertIsNone(task.completed_at, "Дата завершения задачи не была удалена")

        # Проверяем, что сигнал не позволяет завершить задачу неавторизованному пользователю
        with self.assertRaises(PermissionDenied):
            task.worker = self.unauthorized_user
            task.save()

class TaskViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.task = Task.objects.create(
            title="Test Task",
            description="This is a test task",
            deadline=timezone.now() + timezone.timedelta(days=1),
            created_by=self.user,
            worker=self.user,
        )
        self.request_factory = RequestFactory()

    def test_task_update_view_allowed(self):
        request = self.request_factory.get(reverse("tasks:update_task", kwargs={"pk": self.task.pk}))
        request.user = self.user

        setattr(request, "session", "session")
        messages = FallbackStorage(request)
        setattr(request, "_messages", messages)
        response = TaskUpdateView.as_view()(request, pk=self.task.pk)
        self.assertEqual(
            response.status_code,
            200,
            "Доступ к странице редактирования задачи запрещен",
        )

    def test_task_update_view_denied(self):
        another_user = User.objects.create_user(
            username="anotheruser", password="12345"
        )
        request = self.request_factory.get(
            reverse("tasks:update_task", kwargs={"pk": self.task.pk})
        )
        request.user = another_user

        setattr(request, "session", "session")
        messages = FallbackStorage(request)
        setattr(request, "_messages", messages)
        with self.assertRaises(PermissionDenied):
            TaskUpdateView.as_view()(request, pk=self.task.pk)

    def test_task_delete_view_allowed(self):
        request = self.request_factory.post(
            reverse("tasks:delete_task", kwargs={"pk": self.task.pk})
        )
        request.user = self.user

        setattr(request, "session", "session")
        messages = FallbackStorage(request)
        setattr(request, "_messages", messages)
        response = TaskDeleteView.as_view()(request, pk=self.task.pk)
        self.assertEqual(
            response.status_code, 302, "Доступ к странице удаления задачи запрещен"
        )

    def test_task_delete_view_denied(self):
        another_user = User.objects.create_user(
            username="anotheruser", password="12345"
        )
        request = self.request_factory.post(
            reverse("tasks:delete_task", kwargs={"pk": self.task.pk})
        )
        request.user = another_user

        setattr(request, "session", "session")
        messages = FallbackStorage(request)
        setattr(request, "_messages", messages)
        response = TaskDeleteView.as_view()(request, pk=self.task.pk)
        self.assertEqual(
            response.status_code,
            403,
            "Доступ к странице удаления задачи разрешен недопустимому пользователю",
        )
