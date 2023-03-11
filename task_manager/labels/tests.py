import os
import json

from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.db.models import ProtectedError
from django.test import TestCase
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from labels.models import Label
from task_manager.settings import FIXTURE_DIRS


class SetupTestLabels(TestCase):
    fixtures = ['users.json', 'statuses.json', 'labels.json', 'tasks.json']

    def setUp(self):
        self.labels_urls = reverse_lazy('labels')
        self.create_label_url = reverse_lazy('create_label')
        self.update_label1_url = reverse_lazy('update_label', kwargs={'pk': 1})
        self.delete_label1_url = reverse_lazy('delete_label', kwargs={'pk': 1})
        self.delete_label2_url = reverse_lazy('delete_label', kwargs={'pk': 2})
        self.delete_label3_url = reverse_lazy('delete_label', kwargs={'pk': 3})
        self.user1 = get_user_model().objects.get(pk=1)
        self.label1 = Label.objects.get(pk=1)
        with open(os.path.join(FIXTURE_DIRS[0], "test_label1.json")) as file:
            self.test_label = json.load(file)


class TestLabels(SetupTestLabels):
    fixtures = ['users.json', 'statuses.json', 'labels.json', 'tasks.json']

    def test_open_labels_page(self):
        self.client.force_login(self.user1)
        response = self.client.get(self.labels_urls)
        self.assertEqual(response.status_code, 200)

    def test_open_create_lable_page(self):
        self.client.force_login(self.user1)
        response = self.client.get(self.create_label_url)
        self.assertEqual(response.status_code, 200)

    def test_create_label(self):
        labels_count = Label.objects.count()
        self.client.force_login(self.user1)
        response = self.client.post(path=self.create_label_url, data=self.test_label)
        self.assertRedirects(response=response, expected_url=self.labels_urls)
        self.assertEqual(response.status_code, 302)

        self.label4 = Label.objects.get(pk=4)
        self.assertEqual(first=self.label4.name, second=self.test_label.get('name'))
        self.assertEqual(Label.objects.count(), labels_count + 1)

    def test_open_update_label_page(self):
        self.client.force_login(self.user1)
        response = self.client.get(self.update_label1_url)
        self.assertEqual(response.status_code, 200)

    def test_update_label(self):
        self.client.force_login(self.user1)
        self.label1 = Label.objects.get(pk=1)
        self.assertNotEqual(self.label1.name, self.test_label.get("name"))

        response = self.client.post(path=self.update_label1_url, data=self.test_label)
        self.assertEqual(response.status_code, 302)

        self.label1 = Label.objects.get(pk=1)
        self.assertEqual(first=self.label1.name, second=self.test_label.get('name'))

    def test_open_delete_label_page(self):
        self.client.force_login(user=self.user1)
        response = self.client.get(path=self.delete_label1_url)
        self.assertEqual(first=response.status_code, second=200)

    def test_delete_label(self):
        self.client.force_login(user=self.user1)
        response = self.client.delete(path=self.delete_label3_url)
        self.assertEqual(first=response.status_code, second=302)
        with self.assertRaises(Label.DoesNotExist):
            Label.objects.get(pk=3)

    def test_cant_delete_label_with_task(self):
        labels_count = Label.objects.all().count()
        self.client.force_login(user=self.user1)
        with self.assertRaises(expected_exception=ProtectedError):
            self.client.delete(path=self.delete_label1_url)
        self.assertEqual(first=labels_count, second=3)
        response = self.client.post(self.delete_label1_url)
        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertIn(_('It`s not possible to delete the label that is being used'), messages)
