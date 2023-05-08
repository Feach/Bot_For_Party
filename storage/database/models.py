from django.db import models
from django.urls import reverse


class User(models.Model):
    type_user = models.CharField(max_length=50, default="Пользователь")
    name = models.CharField(max_length=50)
    gender = models.CharField(max_length=50)
    age = models.CharField(max_length=50)
    discription = models.TextField(max_length=500)
    user_id = models.CharField(max_length=50)
    inside_id = models.CharField(max_length=50)
    create_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.name


class Party(models.Model):
    title = models.CharField(max_length=50)
    category = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    location = models.CharField(max_length=50)
    age = models.CharField(max_length=50)
    discription = models.TextField(max_length=500)
    users = models.ManyToManyField(User, null=True, blank=True)
    user_now = models.CharField(max_length=10)
    user_max = models.CharField(max_length=10)
    leader_id = models.CharField(max_length=50)
    create_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Пати"
        verbose_name_plural = "Пати"

    def __str__(self):
        return self.title

    def user_count(self):
        return self.users.count()


class StatisticUserCreate(models.Model):
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
    title = models.CharField(max_length=50)
    category = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    location = models.CharField(max_length=50)
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
    title = models.CharField(max_length=50)
    category = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    location = models.CharField(max_length=50)
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

