from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


full_name_validator = RegexValidator(
    regex=r'^[\w.@+\- ]+\Z',
    message='Введите корректное имя. Допустимы буквы, цифры, пробел и символы @/./+/-/_.',
)


class User(AbstractUser):
    username = models.CharField(
        max_length=150,
        validators=[full_name_validator],
        verbose_name='Имя',
        help_text='Введите имя или ФИО. Допустимы буквы, цифры, пробел и символы @/./+/-/_.',
    )
    email = models.EmailField(unique=True, max_length=255)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email
