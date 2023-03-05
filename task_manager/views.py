from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render


def index(request):
    return render(request, 'task_manager/index.html')


class LoginUser(SuccessMessageMixin, LoginView):
    form_class = AuthenticationForm
    template_name = 'task_manager/login'
    success_message = 'Вы залогинены'


class LogoutUser(SuccessMessageMixin, LogoutView):
    def get(self, request, *args, **kwargs):
        messages.info(request, 'Вы разлогинены')
        return super().get(request, *args, **kwargs)
