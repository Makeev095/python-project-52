from django.contrib.auth import get_user_model
from django.forms import TextInput, PasswordInput
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()


class UserForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password1', 'password2']
        widgets = {
            'first_name': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите имя',
                'maxlength': '150'
            }),
            'last_name': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите фамилию',
                'maxlength': '150'
            }),
            'username': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите имя пользователя',
                'maxlength': '150'
            }),
            'password1': PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'Пароль',
                'maxlength': '150'
            }),
            'password2': PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'Подтверждение пароля',
                'maxlength': '150'
            }),
        }