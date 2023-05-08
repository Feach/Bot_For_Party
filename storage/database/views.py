# Файл со всеми вьюхами, который делаю запросы в бд
import requests
from rest_framework import serializers, response, views, status
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from . import models, serializators
from .serializators import PartySerializator


class PartyListPagination(PageNumberPagination):
    page_size = 4
    page_size_query_param = 'page_size'
    max_page_size = 1000


# Получение списка пати
class PartyListView(ListAPIView):
    queryset = models.Party.objects.all().prefetch_related("users")
    pagination_class = PartyListPagination
    serializer_class = PartySerializator


class PartyListWithFilterOnlyCity(ListAPIView):
    pagination_class = PartyListPagination
    serializer_class = PartySerializator

    def get_queryset(self):
        city = self.kwargs.get("city")
        return models.Party.objects.filter(city=city).prefetch_related("users").order_by('pk')


class PartyListWithFilterCategory(ListAPIView):
    pagination_class = PartyListPagination
    serializer_class = PartySerializator

    def get_queryset(self):
        category = self.kwargs.get("category")
        return models.Party.objects.filter(category=category).prefetch_related("users").order_by('pk')


class PartyListWithFilterCategoryAndCity(ListAPIView):
    print('view')
    pagination_class = PartyListPagination
    serializer_class = PartySerializator

    def get_queryset(self):
        city = self.kwargs.get("city")
        category = self.kwargs.get("category")
        return models.Party.objects.filter(category=category, city=city).prefetch_related("users").order_by('pk')


# Получение списка юзеров
class UserListView(views.APIView):

    def get(self, *args, **kwargs):
        users = models.User.objects.all()
        serialized_users = serializators.UserSerializator(users, many=True)
        return response.Response(serialized_users.data)


# Создание юзера по команде /create_user
class CreateUserView(views.APIView):

    def post(self, request, format=None):
        name = request.data.get('name')
        gender = request.data.get('gender')
        age = request.data.get('age')
        discription = request.data.get('discription')
        user_id = request.data.get('user_id')
        inside_id = request.data.get('inside_id')
        models.User.objects.create(name=name,
                                   gender=gender,
                                   age=age,
                                   discription=discription,
                                   user_id=user_id,
                                   inside_id=inside_id
                                   )
        return Response('test', status=status.HTTP_201_CREATED)


class UpdateProfileView(views.APIView):

    def post(self, request, *args, **kwargs):
        name = request.data.get('name')
        gender = request.data.get('gender')
        age = request.data.get('age')
        discription = request.data.get('discription')
        user_id = request.data.get('user_id')
        models.User.objects.filter(user_id=user_id).update(
            name=name,
            gender=gender,
            age=age,
            discription=discription,
            user_id=user_id
            )
        return Response('test', status=status.HTTP_201_CREATED)


# Создание пати по команде /create_party
class CreatePartyView(views.APIView):

    def post(self, request, format=None):
        title = request.data.get('title')
        category = request.data.get('category')
        city = request.data.get('city')
        location = request.data.get('location')
        age = request.data.get('age')
        discription = request.data.get('discription')
        default_users = request.data.get('default_users')
        max_users = request.data.get('max_users')
        leader_id = request.data.get('leader_id')
        models.Party.objects.create(title=title,
                                    category=category,
                                    city=city,
                                    location=location,
                                    age=age,
                                    discription=discription,
                                    user_now=default_users,
                                    user_max=max_users,
                                    leader_id=leader_id
                                    )
        #Подключение создателя в список пользователей
        user_id = request.data.get("leader_id")
        user = models.User.objects.get(user_id=user_id)
        models.Party.objects.get(leader_id=leader_id).users.add(user)
        return Response('test', status=status.HTTP_201_CREATED)


# Подключение пользователя к пати на его выбор
class ConnectToPartyView(views.APIView):
    def post(self, request, format=None):

        party_pk = request.data.get("party_pk")
        user_id = request.data.get("user_id")
        user = models.User.objects.get(user_id=user_id)
        models.Party.objects.get(pk=party_pk).users.add(user)

        return Response('test', status=status.HTTP_201_CREATED)


class DeleteUserView(views.APIView):
    def delete(self, request, pk, format=None):
        user = models.User.objects.get(pk=pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class DeletePartyView(views.APIView):
    def delete(self, request, pk, format=None):
        party = models.Party.objects.get(pk=pk)
        party.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class DeleteFromPartyView(views.APIView):
    def delete(self, request, format=None):

        party_pk = request.data.get("party_pk")
        user_id = request.data.get("user_id")
        user = models.User.objects.get(user_id=user_id)
        print(user, party_pk)
        models.Party.objects.get(pk=party_pk).users.remove(user)

        return Response(status=status.HTTP_204_NO_CONTENT)


class StatisticCreateUserView(views.APIView):
    def post(self, request, format=None):
        name = request.data.get('name')
        gender = request.data.get('gender')
        age = request.data.get('age')
        discription = request.data.get('discription')
        user_id = request.data.get('user_id')
        inside_id = request.data.get('inside_id')
        models.StatisticUserCreate.objects.create(name=name,
                                   gender=gender,
                                   age=age,
                                   discription=discription,
                                   user_id=user_id,
                                   inside_id=inside_id
                                   )
        return Response('test', status=status.HTTP_201_CREATED)


class StatisticCreatePartyView(views.APIView):

    def post(self, request, format=None):
        title = request.data.get('title')
        category = request.data.get('category')
        city = request.data.get('city')
        location = request.data.get('location')
        age = request.data.get('age')
        discription = request.data.get('discription')
        default_users = request.data.get('default_users')
        max_users = request.data.get('max_users')
        leader_id = request.data.get('leader_id')
        models.StatisticPartyCreate.objects.create(title=title,
                                                   category=category,
                                                   city=city,
                                                   location=location,
                                                   age=age,
                                                   discription=discription,
                                                   user_now=default_users,
                                                   user_max=max_users,
                                                   leader_id=leader_id
                                                   )
        return Response('test', status=status.HTTP_201_CREATED)


class StatisticDeleteUserView(views.APIView):
    def post(self, request, format=None):
        name = request.data.get('name')
        gender = request.data.get('gender')
        age = request.data.get('age')
        discription = request.data.get('discription')
        user_id = request.data.get('user_id')
        inside_id = request.data.get('inside_id')
        models.StatisticUserDelete.objects.create(name=name,
                                   gender=gender,
                                   age=age,
                                   discription=discription,
                                   user_id=user_id,
                                   inside_id=inside_id
                                   )
        return Response('test', status=status.HTTP_201_CREATED)


class StatisticDeletePartyView(views.APIView):

    def post(self, request, format=None):
        title = request.data.get('title')
        category = request.data.get('category')
        city = request.data.get('city')
        location = request.data.get('location')
        age = request.data.get('age')
        discription = request.data.get('discription')
        default_users = request.data.get('default_users')
        max_users = request.data.get('max_users')
        leader_id = request.data.get('leader_id')
        models.StatisticPartyCreate.objects.create(title=title,
                                                   category=category,
                                                   city=city,
                                                   location=location,
                                                   age=age,
                                                   discription=discription,
                                                   user_now=default_users,
                                                   user_max=max_users,
                                                   leader_id=leader_id
                                                   )
        return Response('test', status=status.HTTP_201_CREATED)

