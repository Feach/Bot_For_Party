# Модуль моделей базы данных Django
from django.db import models


class User(models.Model):
    """Класс модели Юзеров"""
    type_user = models.CharField(max_length=50, default="Пользователь", verbose_name="Тип пользователя")
    name = models.CharField(max_length=50, verbose_name="Имя")
    gender = models.CharField(max_length=50, verbose_name="Пол")
    age = models.CharField(max_length=50, verbose_name="Возраст")
    discription = models.TextField(max_length=500, verbose_name="Описание")
    user_id = models.CharField(max_length=50, verbose_name="ID")
    inside_id = models.CharField(max_length=50, verbose_name="Внутренний код")
    create_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата созд")

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.name


class Party(models.Model):
    """Класс модели Пати"""

    title = models.CharField(max_length=50, verbose_name="Тема")
    category = models.CharField(max_length=50, verbose_name="Категория")
    city = models.CharField(max_length=50, verbose_name="Город")
    choice = models.CharField(max_length=50, verbose_name="Тип локации")
    location = models.CharField(max_length=50, verbose_name="Локация")
    lat = models.CharField(max_length=50, verbose_name="Координаты")
    lon = models.CharField(max_length=50, verbose_name="Координаты")
    age = models.CharField(max_length=50, verbose_name="Средний возраст пати")
    discription = models.TextField(max_length=500, verbose_name="Описание")
    users = models.ManyToManyField(User, null=True, blank=True)
    user_now = models.CharField(max_length=10)
    user_max = models.CharField(max_length=10, verbose_name="Максимальное кол-во юзеров")
    leader_id = models.CharField(max_length=50, verbose_name="Ник Лидера")
    create_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Пати"
        verbose_name_plural = "Пати"

    def __str__(self):
        return self.title

    def user_count(self):
        return self.users.count()


class StatisticUserCreate(models.Model):
    """Класс модели созданных Юзеров для статистики"""
    type_user = models.CharField(max_length=50, default="Пользователь")
    name = models.CharField(max_length=50)
    gender = models.CharField(max_length=50)
    age = models.CharField(max_length=50)
    discription = models.TextField(max_length=500)
    user_id = models.CharField(max_length=50)
    inside_id = models.CharField(max_length=50)
    create_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Статистика созданных пользователей"
        verbose_name_plural = "Статистика созданных пользователей"

    def __str__(self):
        return self.name


class StatisticPartyCreate(models.Model):
    """Класс модели созданных Пати для статистики"""

    title = models.CharField(max_length=50)
    category = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    location = models.CharField(max_length=50)
    lat = models.CharField(max_length=50, blank=True)
    lon = models.CharField(max_length=50, blank=True)
    age = models.CharField(max_length=50)
    discription = models.TextField(max_length=500)
    users = models.ManyToManyField(User, null=True, blank=True)
    user_now = models.CharField(max_length=10)
    user_max = models.CharField(max_length=10)
    leader_id = models.CharField(max_length=50)
    create_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Статистика созданных пати"
        verbose_name_plural = "Статистика созданных пати"

    def __str__(self):
        return self.title

    def user_count(self):
        return self.users.count()


class StatisticUserDelete(models.Model):
    """Класс модели удаленных Юзеров для статистики"""

    type_user = models.CharField(max_length=50, default="Пользователь")
    name = models.CharField(max_length=50)
    gender = models.CharField(max_length=50)
    age = models.CharField(max_length=50)
    discription = models.TextField(max_length=500)
    user_id = models.CharField(max_length=50)
    inside_id = models.CharField(max_length=50)
    create_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Статистика удаленных пользователей"
        verbose_name_plural = "Статистика удаленных пользователей"

    def __str__(self):
        return self.name


class StatisticPartyDelete(models.Model):
    """Класс модели удаленных Пати для статистики"""

    title = models.CharField(max_length=50)
    category = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    location = models.CharField(max_length=50)
    lat = models.CharField(max_length=50, blank=True)
    lon = models.CharField(max_length=50, blank=True)
    age = models.CharField(max_length=50)
    discription = models.TextField(max_length=500)
    users = models.ManyToManyField(User, null=True, blank=True)
    user_now = models.CharField(max_length=10)
    user_max = models.CharField(max_length=10)
    leader_id = models.CharField(max_length=50)
    create_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Статистика удаленных пати"
        verbose_name_plural = "Статистика удаленных пати"

    def __str__(self):
        return self.title

    def user_count(self):
        return self.users.count()

