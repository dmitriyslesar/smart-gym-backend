from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

class Order(models.Model):
    STATUS_CHOICES = (
        ('Новый', 'Новый'),
        ('Подтвержден', 'Подтвержден'),
        ('Выполнен', 'Выполнен'),
        ('Отменен', 'Отменен'),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    total_price = models.IntegerField()

    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default='Новый'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f'Заказ №{self.id}'


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items'
    )

    product_name = models.CharField(max_length=255)

    quantity = models.IntegerField()

    price = models.IntegerField()

    def __str__(self):
        return self.product_name

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
