# Модуль классов представления моделей базы данных Django
from rest_framework import response, views, status
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from . import models, serializators
from .serializators import PartySerializator


class PartyListPagination(PageNumberPagination):
    """Класс пагинации списка Пати"""
    page_size = 1
    page_size_query_param = 'page_size'
    max_page_size = 1000


class PartyListView(ListAPIView):
    """Класс получения объектов из таблицы Пати"""
    queryset = models.Party.objects.all().prefetch_related("users")
    pagination_class = PartyListPagination
    serializer_class = PartySerializator


class PartyListWithFilterOnlyCity(ListAPIView):
    """Класс получения объектов из таблицы Пати с фильтрацией только по городам"""

    pagination_class = PartyListPagination
    serializer_class = PartySerializator

    def get_queryset(self):
        city = self.kwargs.get("city")
        return models.Party.objects.filter(city=city).prefetch_related("users").order_by('pk')


class PartyListWithFilterCategory(ListAPIView):
    """Класс получения объектов из таблицы Пати с фильтрацией только по категории"""

    pagination_class = PartyListPagination
    serializer_class = PartySerializator

    def get_queryset(self):
        category = self.kwargs.get("category")
        return models.Party.objects.filter(category=category).prefetch_related("users").order_by('pk')


class PartyListWithFilterCategoryAndCity(ListAPIView):
    """Класс получения объектов из таблицы Пати с фильтрацией по категории и городу"""

    pagination_class = PartyListPagination
    serializer_class = PartySerializator

    def get_queryset(self):
        city = self.kwargs.get("city")
        category = self.kwargs.get("category")
        return models.Party.objects.filter(category=category, city=city).prefetch_related("users").order_by('pk')


class UserListView(views.APIView):
    """Класс получения объектов из таблицы Юзеров"""

    def get(self, *args, **kwargs):
        users = models.User.objects.all()
        serialized_users = serializators.UserSerializator(users, many=True)
        return response.Response(serialized_users.data)


class CreateUserView(views.APIView):
    """Класс создания объектов в таблице Юзеров"""

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
    """Класс изменения объектов в таблице Юзеров"""

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


class CreatePartyView(views.APIView):
    """Класс создания объектов в таблице Пати и добавление лидера в число юзеров созданной пати"""

    def post(self, request, format=None):
        title = request.data.get('title')
        category = request.data.get('category')
        city = request.data.get('city')
        choice = request.data.get('choice')
        location = request.data.get('location')
        lat = request.data.get('lat')
        lon = request.data.get('lon')
        age = request.data.get('age')
        discription = request.data.get('discription')
        default_users = request.data.get('default_users')
        max_users = request.data.get('max_users')
        leader_id = request.data.get('leader_id')
        models.Party.objects.create(title=title,
                                    category=category,
                                    city=city,
                                    choice=choice,
                                    location=location,
                                    lat=lat,
                                    lon=lon,
                                    age=age,
                                    discription=discription,
                                    user_now=default_users,
                                    user_max=max_users,
                                    leader_id=leader_id
                                    )
        user_id = request.data.get("leader_id")
        user = models.User.objects.get(user_id=user_id)
        models.Party.objects.get(leader_id=leader_id).users.add(user)
        return Response('test', status=status.HTTP_201_CREATED)


class ConnectToPartyView(views.APIView):
    """Класс подключения Юзеров к Пати"""

    def post(self, request, format=None):
        party_pk = request.data.get("party_pk")
        user_id = request.data.get("user_id")
        user = models.User.objects.get(user_id=user_id)
        models.Party.objects.get(pk=party_pk).users.add(user)

        return Response('test', status=status.HTTP_201_CREATED)


class DeleteUserView(views.APIView):
    """Класс удаления объектов в таблице Юзеров"""
    def delete(self, request, pk, format=None):
        user = models.User.objects.get(pk=pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class DeletePartyView(views.APIView):
    """Класс удаления объектов в таблице Пати"""

    def delete(self, request, pk, format=None):
        party = models.Party.objects.get(pk=pk)
        party.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class DeleteFromPartyView(views.APIView):
    """Класс удаления Юзеров в из участников Пати"""

    def delete(self, request, format=None):

        party_pk = request.data.get("party_pk")
        user_id = request.data.get("user_id")
        user = models.User.objects.get(user_id=user_id)
        print(user, party_pk)
        models.Party.objects.get(pk=party_pk).users.remove(user)

        return Response(status=status.HTTP_204_NO_CONTENT)


class StatisticCreateUserView(views.APIView):
    """Класс создания объектов в таблице Юзеров для статистики"""

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
    """Класс создания объектов в таблице Пати для статистики"""

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
    """Класс создания удаленных объектов в таблице Юзеров для статистики"""

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
    """Класс создания удаленных объектов в таблице Пати для статистики"""


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

