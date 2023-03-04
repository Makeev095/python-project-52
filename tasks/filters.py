import django_filters
from django import forms
from django_filters import filters
from labels.models import Label
from statuses.models import Status
from tasks.models import Task
from users.models import CustomUser
from django.utils.translation import gettext as _


class TaskFilter(django_filters.FilterSet):

    def choose_author(self, queryset, name, value):
        if value:
            author = getattr(self.request, 'user', None)
            return queryset.filter(author=author)
        return queryset

    status = filters.ModelChoiceFilter(queryset=Status.objects.all(), label=_('Status'))
    executor = filters.ModelChoiceFilter(queryset=CustomUser.objects.all(), label=_('Executor'))
    labels = filters.ModelChoiceFilter(queryset=Label.objects.all(), label=_('Label'))
    self_author = filters.BooleanFilter(
        field_name='author',
        widget=forms.widgets.CheckboxInput(
            attrs={'class': 'form-check'}
        ),
        label=_('Only your tasks'),
        method='choose_author'
    )

    class Meta:
        model = Task
        fields = ['status', 'executor', 'labels']