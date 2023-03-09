

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from django.utils.translation import gettext_lazy as _

from task_manager.mixin import AuthRequiredMixin, UserPermissionMixin
from tasks.models import Task
from .forms import UserForm
from .models import CustomUser


class UserList(ListView):
    model = get_user_model()
    template_name = "users/users.html"
    context_object_name = "users"
    extra_context = {'title': _('Users'),
                     'btn_update': _('Update'),
                     'btn_delete': _('Delete'),
                     }


class RegisterUser(SuccessMessageMixin, CreateView):
    model = CustomUser
    form_class = UserForm
    template_name = 'users/create.html'
    success_url = reverse_lazy('login')
    success_message = _('User successfully registered')
    extra_context = {'title': _('Registration user'),
                     'btn_name': _('Register')
                     }


class UpdateUser(UserPermissionMixin, AuthRequiredMixin, SuccessMessageMixin, UpdateView):
    model = CustomUser
    form_class = UserForm
    template_name = 'users/update.html'
    success_url = reverse_lazy('users')
    success_message = _('User successfully updated')
    extra_context = {'title': _('Update user'),
                     'btn_name': _('Update'),
                     }


class DeleteUser(UserPermissionMixin, AuthRequiredMixin, SuccessMessageMixin, DeleteView):
    model = CustomUser
    template_name = 'users/delete.html'
    success_url = reverse_lazy('users')
    success_message = _('User successfully deleted')
    extra_context = {'title': _('Delete user'),
                     'btn_name': _('Yes, delete'),
                     }

    def post(self, request, *args, **kwargs):
        self_id = self.kwargs['pk']
        if Task.objects.filter(
                Q(executor_id=self_id) | Q(author_id=self_id)):
            messages.error(
                self.request,
                _('It`s not possible to delete a User that is being used')
            )
            return redirect(self.success_url)
        return super().post(request, *args, **kwargs)
