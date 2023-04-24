from django.contrib import admin
from django.urls import path

from database import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('create_party/', views.CreatePartyView.as_view()),
    path('delete_party/<int:pk>/', views.DeletePartyView.as_view()),
    path('delete_from_party/', views.DeleteFromPartyView.as_view()),
    path('connect_to_party/', views.ConnectToPartyView.as_view()),
    path('party_list/', views.PartyListView.as_view()),
    path('party_list/<str:city>/', views.PartyListWithFilter.as_view(), name="party_list_with_filter"),
    path('users/', views.UserListView.as_view()),
    path('update_profile/', views.UpdateProfileView.as_view()),
    path('create_users/', views.CreateUserView.as_view()),
    path('delete_users/<int:pk>/', views.DeleteUserView.as_view()),
]
