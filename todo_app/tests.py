from django.test import TestCase, Client
from django.urls import reverse
from .models import Task

class TaskModelTest(TestCase):
    def test_task_creation(self):
        task = Task.objects.create(title="Test Task")
        self.assertTrue(isinstance(task, Task))
        self.assertEqual(task.__str__(), "Test Task")
        self.assertFalse(task.completed)

class TaskViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.task = Task.objects.create(title="Test Task")
        self.list_url = reverse('task_list')
        self.create_url = reverse('task_create')
        self.update_url = reverse('task_update', args=[self.task.pk])
        self.delete_url = reverse('task_delete', args=[self.task.pk])

    def test_task_list_view(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Task")

    def test_task_create_view(self):
        response = self.client.post(self.create_url, {'title': 'New Task'})
        self.assertEqual(response.status_code, 302) # Redirects after success
        self.assertEqual(Task.objects.count(), 2)

    def test_task_update_view(self):
        # Test marking as complete
        response = self.client.post(self.update_url, {'completed': 'true'})
        self.assertEqual(response.status_code, 302)
        self.task.refresh_from_db()
        self.assertTrue(self.task.completed)

        # Test title update
        response = self.client.post(self.update_url, {'title': 'Updated Task'})
        self.assertEqual(response.status_code, 302)
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, 'Updated Task')

    def test_task_delete_view(self):
        response = self.client.post(self.delete_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Task.objects.count(), 0)
