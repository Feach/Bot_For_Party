from django.contrib import admin

from . import models


class UserAdmin(admin.ModelAdmin):
    list_display = ['pk', 'type_user', 'name', 'gender', 'age', 'discription', 'user_id', 'inside_id', 'create_at']
    # list_editable = ['gender', 'age', 'discription', 'user_id'] редактирование полей в админке


class PartyAdmin(admin.ModelAdmin):
    list_display = ['pk', 'category', 'title', 'city', 'location', 'age', 'discription', 'user_count', 'user_max', 'leader_id', 'create_at']
    filter_horizontal = ['users']


class StatisticUserCreateAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name', 'gender', 'age', 'user_id', 'inside_id', 'create_at']
    # list_editable = ['gender', 'age', 'discription', 'user_id'] редактирование полей в админке


class StatisticPartyCreateAdmin(admin.ModelAdmin):
    list_display = ['pk', 'category', 'city', 'location', 'age', 'user_max', 'leader_id', 'create_at']


class StatisticUserDeleteAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name', 'gender', 'age', 'user_id', 'inside_id', 'create_at']
    # list_editable = ['gender', 'age', 'discription', 'user_id'] редактирование полей в админке


class StatisticPartyDeleteAdmin(admin.ModelAdmin):
    list_display = ['pk', 'category', 'city', 'location', 'age', 'user_max', 'leader_id', 'create_at']


admin.site.register(models.User, UserAdmin)
admin.site.register(models.Party, PartyAdmin)
admin.site.register(models.StatisticUserCreate, StatisticUserCreateAdmin)
admin.site.register(models.StatisticPartyCreate, StatisticPartyCreateAdmin)
admin.site.register(models.StatisticUserDelete, StatisticUserDeleteAdmin)
admin.site.register(models.StatisticPartyDelete, StatisticPartyDeleteAdmin)

