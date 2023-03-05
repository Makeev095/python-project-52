import os
import json

from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse_lazy
from tasks.models import Task
from task_manager.settings import FIXTURE_DIRS
from django.utils.translation import gettext_lazy as _


class SetupTestTasks(TestCase):
    fixtures = ['users.json', 'tasks.json', 'labels.json', 'statuses.json']

    def setUp(self):
        self.tasks_url = reverse_lazy('tasks')
        self.login_url = reverse_lazy('login')
        self.create_task_url = reverse_lazy('create_task')
        self.update_task_url = reverse_lazy("update_task", kwargs={"pk": 1})
        self.delete_task1_url = reverse_lazy("delete_task", kwargs={"pk": 1})
        self.delete_task2_url = reverse_lazy("delete_task", kwargs={"pk": 2})
        self.user1 = get_user_model().objects.get(pk=1)
        self.task1 = Task.objects.get(pk=1)
        self.task2 = Task.objects.get(pk=2)
        with open(os.path.join(FIXTURE_DIRS[0], "test_task1.json")) as file:
            self.test_task = json.load(file)


class TestTask(SetupTestTasks):
    fixtures = ['users.json', 'tasks.json', 'labels.json', 'statuses.json']

    def test_open_create_task_page(self):
        self.client.force_login(user=self.user1)
        response = self.client.get(self.create_task_url)
        self.assertEqual(first=response.status_code, second=200)

    def test_open_all_tasks_page(self):
        self.client.force_login(user=self.user1)
        response = self.client.get(self.tasks_url)
        self.assertEqual(first=response.status_code, second=200)

    def test_create_task(self):
        task_count = Task.objects.count()
        self.client.force_login(self.user1)
        response = self.client.post(path=self.create_task_url, data=self.test_task)
        self.assertEqual(response.status_code, 302)
        self.task3 = Task.objects.get(pk=3)
        self.assertEqual(first=self.task3.name, second=self.test_task.get('name'))
        self.assertEqual(Task.objects.count(), task_count + 1)

    def test_open_update_tasks_page(self):
        self.client.force_login(user=self.user1)
        response = self.client.get(self.update_task_url)
        self.assertEqual(first=response.status_code, second=200)

    def test_update_task(self):

        self.client.force_login(self.user1)
        self.assertNotEqual(first=self.task1.name,
                            second=self.test_task.get("name"))

        response = self.client.post(path=self.update_task_url, data=self.test_task)
        self.assertEqual(first=response.status_code, second=302)

        self.task = Task.objects.get(pk=1)
        self.assertEqual(first=self.task.name,
                         second=self.test_task.get('name'))

    def test_open_delete_page(self):
        self.client.force_login(user=self.user1)
        response = self.client.get(path=self.delete_task1_url)
        self.assertEqual(first=response.status_code, second=200)

    def test_delete_task(self):
        task_count = Task.objects.count()
        self.client.force_login(user=self.user1)
        response = self.client.delete(path=self.delete_task1_url)
        self.assertEqual(first=response.status_code, second=302)
        task_count_after_delete = Task.objects.count()
        self.assertGreater(task_count, task_count_after_delete)
        with self.assertRaises(expected_exception=Task.DoesNotExist):
            Task.objects.get(pk=1)

    def test_cant_delete_task_if_user_is_not_author(self):
        task_count = Task.objects.count()
        self.client.force_login(user=self.user1)
        response = self.client.delete(path=self.delete_task2_url)
        self.assertEqual(first=response.status_code, second=302)
        self.assertRedirects(response=response, expected_url=self.tasks_url)
        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertIn(_('A task can only be deleted by its author.'), messages)
        self.assertEqual(first=Task.objects.all().count(), second=task_count)
