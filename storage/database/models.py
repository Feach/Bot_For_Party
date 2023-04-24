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

    def __str__(self):
        return self.name


class Party(models.Model):
    title = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    location = models.CharField(max_length=50)
    age = models.CharField(max_length=50)
    discription = models.TextField(max_length=500)
    users = models.ManyToManyField(User, null=True, blank=True)
    user_now = models.CharField(max_length=10)
    user_max = models.CharField(max_length=10)
    leader_id = models.CharField(max_length=50)
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def user_count(self):
        return self.users.count()



