# Модуль классов для отображения моделей в админ-панели django
from django.contrib import admin

from . import models


class UserAdmin(admin.ModelAdmin):
    """Класс Юзеров в админ панели"""
    list_display = ['pk', 'type_user', 'name', 'gender', 'age', 'discription', 'user_id', 'inside_id', 'create_at']


class PartyAdmin(admin.ModelAdmin):
    """Класс Пати в админ панели"""
    list_display = ['pk', 'category', 'title', 'city', 'choice', 'location', 'age', 'discription', 'user_count', 'user_max', 'leader_id', 'create_at']
    filter_horizontal = ['users']


admin.site.register(models.User, UserAdmin)
admin.site.register(models.Party, PartyAdmin)
