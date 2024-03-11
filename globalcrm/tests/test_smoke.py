from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.utils import timezone

from tasks.models import Task

User = get_user_model()


class IndexTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username="testuser", password="12345")
        cls.client = Client()
        cls.client.force_login(cls.user)
        task = Task.objects.create(
            title="Test Task",
            description="This is a test task",
            deadline=timezone.now() + timezone.timedelta(days=1),
            created_by=cls.user,
            worker=cls.user,
        )
    
    def test_homepage(self):
        self.client.force_login(self.user)
        response =  self.client.get('/')
        self.assertEqual(response.status_code, 200)
    
    def test_for_me_tasks(self):
        self.client.force_login(self.user)
        response =  self.client.get('/for_me_tasks/')
        self.assertEqual(response.status_code, 200)
