from enum import Enum
from django.utils.translation import gettext as _


class VerboseName(Enum):
    NAME = _('Name')
    STATUS = _('Status')
    EXECUTOR = _('Executor')
    LABEL = _('Label')
    LABELS = _('Labels')
    DESCRIPTION = _('Description')


class FlashMessages(Enum):
    REGISTER_SUCCESS = _('User is successfully registered')
    LOGIN_SUCCESS = _('You are logged in')
    LOGOUT_SUCCESS = _('You are logged out')
