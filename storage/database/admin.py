from django.contrib import admin

from . import models


class UserAdmin(admin.ModelAdmin):
    list_display = ['pk', 'type_user', 'name', 'gender', 'age', 'discription', 'user_id', 'inside_id', 'create_at']
    # list_editable = ['gender', 'age', 'discription', 'user_id'] редактирование полей в админке


class PartyAdmin(admin.ModelAdmin):
    list_display = ['pk', 'title', 'city', 'location', 'age', 'discription', 'user_count', 'user_max', 'leader_id', 'create_at']
    filter_horizontal = ['users']


admin.site.register(models.User, UserAdmin)
admin.site.register(models.Party, PartyAdmin)

