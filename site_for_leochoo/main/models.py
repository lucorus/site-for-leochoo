from django.conf import settings
from django.contrib.auth.models import AbstractUser, User
from django.db import models
from django.shortcuts import redirect
from django.urls import reverse_lazy


class Question(models.Model):
    text = models.TextField(verbose_name='Текст вашего комментария')
    answer_by = models.IntegerField(blank=True, null=True, verbose_name='на какой комментарий вы хотите ответить?')
    #answer_by = models.ForeignKey('CustomUser', on_delete=models.CASCADE, blank=True, null=True, verbose_name='Кому вы хотите написать ответ?', related_name='answer_by')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Автор', related_name='author')
    created_add = models.DateTimeField(auto_now_add=True, verbose_name='Создано')

    def get_absolute_url(self):
        return reverse_lazy('answer_by', kwargs={"answer_by": self.pk})

    def quantity_comments(self, pk):
        comm = Question.objects.filter(id=pk).count()
        if comm > 0:
            return True
        else:
            return False

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'


class CustomUser(AbstractUser):
    username = models.CharField(max_length=40, unique=False, default='', verbose_name='Имя пользователя')
    avatar = models.ImageField(upload_to='photos',  verbose_name='Аватар')
    description = models.CharField(verbose_name='Статус', blank=True, max_length=120)
    information = models.CharField(max_length=200, verbose_name='Информация о пользователе', blank=True, default='')

    def get_absolute_url(self):
        return reverse_lazy('username', kwargs={"username_id": self.pk})

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
