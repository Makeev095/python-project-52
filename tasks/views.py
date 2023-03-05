from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView
from django_filters.views import FilterView
from django.utils.translation import gettext_lazy as _

from task_manager.mixin import TaskPassesTestMixin, MyLoginRequiredMixin
from tasks.filters import TaskFilter
from tasks.forms import TaskForm
from tasks.models import Task


class TaskListView(FilterView):
    model = Task
    template_name = 'tasks/index.html'
    filterset_class = TaskFilter
    context_object_name = "tasks"


class CreateTaskView(SuccessMessageMixin, MyLoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/create.html'
    success_url = reverse_lazy('tasks')
    success_message = _('Task successfully created')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class UpdateTaskView(TaskPassesTestMixin, SuccessMessageMixin, MyLoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/update.html'
    success_url = reverse_lazy('tasks')
    success_message = _('Task successfully updated')


class DeleteTaskView(TaskPassesTestMixin, SuccessMessageMixin, MyLoginRequiredMixin, DeleteView):
    model = Task
    template_name = 'tasks/delete.html'
    success_url = reverse_lazy('tasks')
    success_message = _('Task successfully deleted')


class TaskDetailView(SuccessMessageMixin, MyLoginRequiredMixin, DetailView):
    model = Task
    template_name = "tasks/task.html"
