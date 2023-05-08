from django.shortcuts import render
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response

from database import models


class UserSerializator(serializers.ModelSerializer):

    class Meta:
        model = models.User
        fields = ['pk',
                  'name',
                  'gender',
                  'age',
                  'discription',
                  'user_id',
                  'inside_id'
                  ]


class PartySerializator(serializers.ModelSerializer):
    users = UserSerializator(read_only=True, many=True)

    class Meta:
        model = models.Party
        fields = [
            'pk',
            'title',
            'category',
            'city',
            'location',
            'age',
            'discription',
            'user_count',
            'user_max',
            'leader_id',
            'users'
            ]

    def get_users(self, obj):
        return obj.users.name


