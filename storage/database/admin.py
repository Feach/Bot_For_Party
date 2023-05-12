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


class StatisticUserCreateAdmin(admin.ModelAdmin):
    """Класс созданных Юзеров для статистики в админ панели"""
    list_display = ['pk', 'name', 'gender', 'age', 'user_id', 'inside_id', 'create_at']


class StatisticPartyCreateAdmin(admin.ModelAdmin):
    """Класс созданных Пати для статистики в админ панели"""
    list_display = ['pk', 'category', 'city', 'location', 'age', 'user_max', 'leader_id', 'create_at']


class StatisticUserDeleteAdmin(admin.ModelAdmin):
    """Класс удаленных Юзеров для статистики в админ панели"""
    list_display = ['pk', 'name', 'gender', 'age', 'user_id', 'inside_id', 'create_at']


class StatisticPartyDeleteAdmin(admin.ModelAdmin):
    """Класс удаленных Пати для статистики в админ панели"""
    list_display = ['pk', 'category', 'city', 'location', 'age', 'user_max', 'leader_id', 'create_at']


admin.site.register(models.User, UserAdmin)
admin.site.register(models.Party, PartyAdmin)
admin.site.register(models.StatisticUserCreate, StatisticUserCreateAdmin)
admin.site.register(models.StatisticPartyCreate, StatisticPartyCreateAdmin)
admin.site.register(models.StatisticUserDelete, StatisticUserDeleteAdmin)
admin.site.register(models.StatisticPartyDelete, StatisticPartyDeleteAdmin)

