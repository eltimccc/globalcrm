from django.test import TestCase
from django.utils import timezone
from django.contrib.auth.models import User
from tasks.models import Task, TaskExecution
from django.db.models.signals import pre_save
from django.dispatch import receiver

class TaskModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')

    def test_task_creation(self):
        task = Task.objects.create(
            title="Test Task",
            description="This is a test task",
            deadline=timezone.now() + timezone.timedelta(days=1),
            created_by=self.user,
            worker=self.user
        )

        self.assertEqual(task.title, "Test Task", "Неверное название задачи")
        self.assertEqual(task.description, "This is a test task", "Неверное описание задачи")
        self.assertTrue(task.deadline > timezone.now(), "Дедлайн находится в прошлом")
        self.assertEqual(task.created_by, self.user, "Неверный создатель задачи")
        self.assertEqual(task.worker, self.user, "Неверный исполнитель задачи")
        self.assertFalse(task.completed, "Задача помечена как завершенная")

    def test_task_completion(self):
        task = Task.objects.create(
            title="Test Task",
            description="This is a test task",
            deadline=timezone.now() + timezone.timedelta(days=1),
            created_by=self.user,
            worker=self.user
        )

        task.completed = True
        task.save()

        self.assertTrue(task.completed, "Задача не была помечена как завершенная")
        self.assertIsNotNone(task.completed_at, "Поле completed_at не было заполнено")

    def test_task_execution_creation(self):
        task = Task.objects.create(
            title="Parent Task",
            description="This is a parent task",
            deadline=timezone.now() + timezone.timedelta(days=1),
            created_by=self.user,
            worker=self.user
        )

        execution = TaskExecution.objects.create(
            title="Execution Task",
            description="This is an execution task",
            deadline=timezone.now() + timezone.timedelta(days=1),
            task=task
        )

        self.assertEqual(execution.title, "Execution Task", "Неверное название выполнения задачи")
        self.assertEqual(execution.task, task, "Неверная родительская задача")
        self.assertEqual(execution.description, "This is an execution task", "Неверное описание выполнения задачи")
        self.assertTrue(execution.deadline > timezone.now(), "Дедлайн выполнения задачи находится в прошлом")

    def test_deadline_cannot_be_set_before_today(self):
        today = timezone.now().date()
        yesterday = today - timezone.timedelta(days=1)

        with self.assertRaises(ValueError, msg="Дедлайн задачи был установлен на прошедшую дату"):
            Task.objects.create(
                title="Test Task",
                description="This is a test task",
                deadline=yesterday,
                created_by=self.user,
                worker=self.user
            )

def set_completed_at(instance, **kwargs):
    if instance.completed and not instance.completed_at:
        instance.completed_at = timezone.now()
    elif not instance.completed:
        instance.completed_at = None


class SignalTest(TestCase):
    def test_task_completion_signal(self):
        task = Task.objects.create(
            title="Test Task",
            description="This is a test task",
            deadline=timezone.now() + timezone.timedelta(days=1),
            created_by=User.objects.create(username='testuser'),
            worker=User.objects.create(username='workeruser')
        )

        task.completed = True
        task.save()
        self.assertIsNotNone(task.completed_at, "Дата завершения задачи не была установлена")

        task.completed = False
        task.save()
        self.assertIsNone(task.completed_at, "Дата завершения задачи не была удалена")

