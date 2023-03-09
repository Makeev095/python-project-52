import os
import json

from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import ProtectedError
from django.test import TestCase
from django.urls import reverse_lazy
from statuses.models import Status
from task_manager.settings import FIXTURE_DIRS
from django.utils.translation import gettext_lazy as _


class SetupTestStatuses(TestCase):
    fixtures = ['users.json', 'statuses.json', 'labels.json', 'tasks.json']

    def setUp(self):
        self.statuses_url = reverse_lazy('statuses')
        self.create_status_url = reverse_lazy('create_status')
        self.update_status_url = reverse_lazy("update_status", kwargs={"pk": 1})
        self.delete_status1_url = reverse_lazy("delete_status", kwargs={"pk": 1})
        self.delete_status2_url = reverse_lazy("delete_status", kwargs={"pk": 2})
        self.delete_status3_url = reverse_lazy("delete_status", kwargs={"pk": 3})
        self.user = get_user_model().objects.get(pk=1)
        self.status1 = Status.objects.get(pk=1)
        with open(os.path.join(FIXTURE_DIRS[0], "test_status1.json")) as file:
            self.test_status = json.load(file)


class TestStatuses(SetupTestStatuses):
    fixtures = ['users.json', 'statuses.json', 'labels.json', 'tasks.json']

    def test_open_statuses_page(self):
        self.client.force_login(user=self.user)
        response = self.client.get(self.statuses_url)
        self.assertEqual(response.status_code, 200)

    def test_open_create_status_page(self):
        self.client.force_login(user=self.user)
        response = self.client.get(self.create_status_url)
        self.assertEqual(response.status_code, 200)

    def test_create_status(self):
        self.client.force_login(user=self.user)
        response = self.client.post(path=self.create_status_url, data=self.test_status)
        self.assertRedirects(response=response, expected_url=self.statuses_url)
        self.assertEqual(response.status_code, 302)

        self.status4 = Status.objects.get(pk=4)
        self.assertEqual(first=self.status4.name, second=self.test_status.get('name'))

    def test_open_update_statuses_page(self):
        self.client.force_login(user=self.user)
        response = self.client.get(self.update_status_url)
        self.assertEqual(response.status_code, 200)

    def test_update_status(self):
        self.client.force_login(user=self.user)
        self.assertNotEqual(self.status1.name, self.test_status.get("name"))
        response = self.client.post(path=self.update_status_url, data=self.test_status)
        self.assertEqual(response.status_code, 302)
        self.status1 = Status.objects.get(pk=1)
        self.assertEqual(first=self.status1.name, second=self.test_status.get('name'))

    def test_open_delete_page(self):
        self.client.force_login(user=self.user)
        response = self.client.get(path=self.delete_status1_url)
        self.assertEqual(first=response.status_code, second=200)

    def test_delete_status(self):
        self.client.force_login(user=self.user)
        response = self.client.delete(path=self.delete_status3_url)
        self.assertEqual(first=response.status_code, second=302)
        with self.assertRaises(ObjectDoesNotExist):
            Status.objects.get(pk=3)

    def test_cant_delete_status_with_task(self):
        statuses_count = Status.objects.count()
        self.client.force_login(user=self.user)
        with self.assertRaises(expected_exception=ProtectedError):
            response = self.client.delete(path=self.delete_status1_url)
            messages = [m.message for m in get_messages(response.wsgi_request)]
            self.assertIn(_('It`s not possible to delete the status that is being used'), messages)
        self.assertEqual(first=statuses_count, second=3)
