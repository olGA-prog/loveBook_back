from django.db import models

class CustomUser(models.Model):
    telegram_id = models.IntegerField(unique=True, null=True, blank=True, verbose_name='ТГ ID')
    email = models.EmailField(unique=True, verbose_name="Эл. почта")
    first_name = models.CharField(max_length=200, null=True, verbose_name='Имя')
    last_name = models.CharField(max_length=255, blank=True, null=True, verbose_name='Фамилия')
    address = models.CharField(max_length=300, verbose_name='Адрес')
    username = models.CharField(max_length=255, blank=True, null=True, verbose_name='Имя пользователя')
    phone_number = models.CharField(max_length=20, verbose_name='Номер телефона')
    auth_date = models.DateTimeField(blank=True, null=True, verbose_name='Дата авторизации')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f"{self.telegram_id}{self.first_name}{self.last_name}{self.address} {self.username} ({self.phone_number})"
